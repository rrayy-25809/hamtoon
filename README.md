README: DB 마이그레이션 계획 (DuckDB → PostgreSQL(JSONB))
-------------------------------------------------------

목적
- 기존 DuckDB 기반 웹 서버를 웹용 OLTP에 적합한 데이터베이스로 전환한다.
- JSON-like 객체(유연한 스키마)를 단일 테이블에 저장하면서 높은 동시성, ACID 보장, JSON 내부 필드 인덱싱/쿼리를 지원하는 구조로 마이그레이션한다.
- 기본 권장 대상: PostgreSQL (JSONB). (프로토타입/매니지드 옵션: Supabase / Neon)

범위 및 가정
- 기존 데이터는 DuckDB 파일 한 개 또는 여러 파일에 저장되어 있음.
- 애플리케이션은 객체(문서)를 단일 테이블 컬럼에 저장함(예: payload JSON).
- 다운타임을 최소화하는 절차를 우선 고려하되, 데이터 규모/요구사항에 따라 스냅샷 기간 동안의 짧은 유지보수 창을 선택할 수 있음.
- 운영 환경: 자체 PostgreSQL 또는 managed PostgreSQL (Supabase, Neon, AWS RDS 등).

아키텍처 제안 (간단)
- 테이블: web_data(id PK, payload JSONB NOT NULL, created_at TIMESTAMP DEFAULT now(), ... 필요한 인덱스)
- 인덱스: GIN(payload) + expression indexes on frequently queried fields
- 운영 모드: 애플리케이션은 마이그레이션 완료 후 PostgreSQL로 전환. (단계적 전환: read-replica, dual-write 가능)

샘플 스키마
- 기본 단일 테이블 예시
  CREATE TABLE web_data (
    id BIGSERIAL PRIMARY KEY,
    payload JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
  );
- GIN 인덱스 (전체 JSON 검색)
  CREATE INDEX idx_web_data_payload_gin ON web_data USING GIN (payload);
- 표현식 인덱스 (자주 조회하는 필드)
  CREATE INDEX idx_web_data_status ON web_data ((payload ->> 'status'));
  CREATE INDEX idx_web_data_user_email ON web_data (((payload -> 'user') ->> 'email'));

마이그레이션 단계 (권장)
1) 준비 단계
   - 목표 PostgreSQL 인스턴스 생성(테스트/스테이징/프로덕션).
   - 충분한 디스크/메모리 확보, 백업 정책 수립.
   - 네트워크/접근 권한 설정 (DB 유저, 비밀번호, TLS 등).

2) 스키마 생성
   - 위 샘플 스키마를 기반으로 테이블 생성.
   - 프로덕션 전 테스트 DB에서 스키마 검증.

3) 데이터 추출 (DuckDB → 중간 형식)
   방법 A (권장, 안전): DuckDB에서 CSV로 export( JSON 컬럼은 문자열로 export ), PostgreSQL COPY로 import.
     - DuckDB: export CSV with payload quoted (force quoting payload)
       예) duckdb> COPY (SELECT id, payload::VARCHAR AS payload, created_at FROM old_table) TO 'export.csv' (HEADER, DELIMITER ',', FORCE_QUOTE payload);
     - PostgreSQL: COPY web_data(id, payload, created_at) FROM '/path/export.csv' CSV HEADER;
       (Postgres가 payload 문자열을 JSONB로 자동 파싱; 필요시 ::jsonb 사용)
   방법 B (파이프라인): DuckDB에서 newline-delimited JSON (NDJSON) 생성 후 Python 스크립트로 삽입 (batch insert 또는 COPY via psycopg2).
   방법 C (Parquet): DuckDB → Parquet → Python (pandas/pyarrow) → PostgreSQL. (대용량 안전)

   - 대량 데이터 주의: 배치 크기 조절, 트랜잭션 크기 제한(예: 1000~10000 행 단위) 권장.

4) 데이터 변환(옵션)
   - 필요한 경우 payload 내 필드명 정규화, 날짜 형식 정리, 불필요 필드 제거.
   - 변환 스크립트: Python (pandas + psycopg2), node (pg), 또는 ETL 툴 사용.

5) 데이터 적재
   - 테스트 DB에 소규모로 먼저 적재 → 검증.
   - 실제 적재 시 COPY (CSV) 또는 bulk insert 사용.
   - 예: psql COPY
     COPY web_data(id, payload, created_at) FROM '/path/export.csv' CSV HEADER;
   - 또는 Python bulk 예시 (psycopg2.extras.execute_values).

6) 검증
   - 레코드 수 비교: DuckDB 총행수 vs PostgreSQL 총행수.
   - 샘플 데이터 비교: 랜덤 샘플의 payload 해시/MD5 비교.
   - 쿼리 결과 일치 확인 (중요한 비즈니스 쿼리들).
   - 인덱스 작동 여부 확인 (EXPLAIN ANALYZE).

7) 인덱스 및 성능 튜닝
   - GIN 인덱스 추가: CREATE INDEX ... USING GIN (payload);
   - 표현식 인덱스로 자주 사용하는 경로 최적화.
   - 통계 수집: ANALYZE web_data;
   - 파티셔닝 고려(시간 기반, 범위) — 로그/대용량 테이블의 경우.

8) 절차적 전환 (Cutover)
   옵션 A (짧은 downtime): 애플리케이션을 잠시 쓰기 금지(maintenance mode), 최종 데이터 델타 동기화, PostgreSQL으로 전환.
   옵션 B (무중단/dual-write): 마이그레이션 기간 동안 애플리케이션에서 DuckDB와 PostgreSQL에 동시에 쓰기(동기 복제 레이어 필요). 테스트가 충분하면 점진적 전환 가능.
   - 권장: 소규모/중간 규모 서비스는 짧은 maintenance 창으로 cutover 권장(복잡도 낮음).

9) 롤백 계획
   - PostgreSQL 적재에 문제 발생 시: PostgreSQL 인스턴스를 폐기하거나, 트래픽을 다시 DuckDB 기반 서버로 라우팅(단, DuckDB의 동시성 한계 주의).
   - 반드시 DuckDB 원본 파일/백업을 보존.
   - PostgreSQL으로의 마지막 쓰기 전 스냅샷(백업) 생성.

10) 운영 후 작업
   - 모니터링: pg_stat_activity, pg_stat_user_indexes, pg_stat_statements, slow query log.
   - 정기 VACUUM/ANALYZE, 인덱스 리빌드 정책.
   - 백업 & 복구 테스트(Restore 연습).
   - 필요 시 리팩토링: 특정 쿼리의 성능 문제를 파악하고 expression index 또는 정규화(일부 필드를 컬럼화) 결정.

검증 체크리스트 (예)
- [ ] 총행수 일치
- [ ] 랜덤 샘플 100건 JSON 해시 일치
- [ ] 주요 비즈니스 쿼리 결과 일치
- [ ] 인덱스 생성 및 쿼리 플랜 확인
- [ ] 성능 벤치: 읽기/쓰기 latency 측정
- [ ] 백업/복구 시나리오 검증

예제: 간단한 Python bulk 업로드 스크립트 (아이디어)
- Python (psycopg2)로 NDJSON 읽어 batch insert
  import json, psycopg2
  from psycopg2.extras import execute_values

  conn = psycopg2.connect("postgresql://user:pass@host/db")
  cur = conn.cursor()
  batch = []
  BATCH_SIZE = 1000
  with open("export.ndjson") as f:
      for line in f:
          payload = json.loads(line)
          batch.append((json.dumps(payload),))  # payload column only
          if len(batch) >= BATCH_SIZE:
              execute_values(cur, "INSERT INTO web_data (payload) VALUES %s", batch)
              conn.commit()
              batch = []
  if batch:
      execute_values(cur, "INSERT INTO web_data (payload) VALUES %s", batch)
      conn.commit()

성능/인덱싱 팁
- GIN 인덱스는 JSONB 전체 검색에 유리하나 인덱스 크기/쓰기 비용 고려.
- 자주 필터/정렬하는 JSON 경로는 expression index로 뽑아 컬럼화 검토.
- 대용량 I/O 작업 시 WAL/replication 비용을 줄이려면 적재 중 일시적으로 synchronous_commit을 완화하거나 unlogged table을 활용 후 안전한 마이그레이션 전략 적용(리스크 주의).

타임라인(예시)
- 소규모(수만 건): 준비/테스트(1일), 마이그레이션(1시간), 검증(1일).
- 중간 규모(수백만 건): 준비/테스트(1~3일), 변환/적재(수시간~1일), 검증(1~2일).
- 대규모(수억 건): 별도 ETL 파이프라인, 파티셔닝/병렬 적재 설계 필요(수주).

추가 권장 사항
- 프로토타입으로 Supabase 또는 Neon 사용해 빠르게 테스트해보세요(관리형으로 운영 부담 감소).
- 중요한 쿼리와 사용 패턴을 먼저 파악하여, 표현식 인덱스 또는 컬럼화 우선순위를 정하세요.
- DuckDB는 분석 목적(OLAP)에 계속 활용 가능(ETL, 백오프 데이터 소스로서).

문의 및 책임
- 이 계획은 일반적인 권장사항입니다. 데이터 특성(스키마, 크기, 쿼리패턴)에 따라 세부 조정이 필요합니다.
- 필요하시면 실제 DuckDB 데이터 샘플(비민감 데이터)로 마이그레이션 스크립트 템플릿을 만들어 드리겠습니다.

끝.

원하시면 이 README를 실제 파일로 생성해 드리거나(프로젝트 루트에 README.md로 저장), DuckDB → PostgreSQL 샘플 스크립트를 구체적으로 만들어 드릴게요. 어떤 옵션을 원하시요?