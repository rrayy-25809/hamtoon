const listElement = document.getElementById('list') as HTMLDivElement;

// simple debounce to avoid firing requests on every keystroke
function debounce<T extends (...args: any[]) => void>(fn: T, wait = 300) {
  let timer: number | undefined;
  return (...args: any[]) => {
    if (timer) window.clearTimeout(timer);
    timer = window.setTimeout(() => fn(...args), wait) as unknown as number;
  };
}

async function getToday(keyword: string): Promise<string> {
  let webtoon:string = '';
  const response = await fetch("/today", {
    method: "POST"
  });
  if (response.ok) {
    const data = await response.json();
    data.forEach((item: any) => {
      if (!keyword || item['title'].includes(keyword)) {
        webtoon += `
        <a href="/webtoon/${item['id']}">
          <div class="col">
            <div class="card" style="margin-top: 10px;">
              <img src="${item["thumb"]}" class="card-img-top" alt="...">
              <div class="card-body">
                <h5 class="card-title">${item['title']}</h5>
              </div>
            </div>
          </div>
        </a>
        `;
      }
    });
  } else {
    alert("정보를 불러오는데 실패했습니다.");
  }
  return webtoon;
}

getToday("").then(result => {
  listElement.innerHTML = result;
});

function searchWebtoon() {
  const input = document.getElementById('search-input') as HTMLInputElement | null;
  listElement.innerHTML = '<div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div>';
  const keyword = input ? input.value : '';
  getToday(keyword).then(result => {
    listElement.innerHTML = result;
  });
}

// attach debounced input listener if the element exists
document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('search-input') as HTMLInputElement | null;
  if (input) {
    input.addEventListener('input', debounce(() => searchWebtoon(), 300));
  }
});