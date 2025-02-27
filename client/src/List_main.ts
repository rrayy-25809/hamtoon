const listElement = document.getElementById('list') as HTMLDivElement;

async function getToday(): Promise<string> {
  let webtoon:string = '';
  const response = await fetch("/today", {
    method: "POST"
  });
  if (response.ok) {
    const data = await response.json();
    console.log(data);
    data.forEach((item: any) => {
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
    });
  } else {
    alert("정보를 불러오는데 실패했습니다.");
  }
  return webtoon;
}

getToday().then(result => {
  listElement.innerHTML = result;
});