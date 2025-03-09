const webtoon_id = location.href.split("/")[4];
const listElement = document.getElementById('episode-list') as HTMLDivElement;

async function getEpisode(): Promise<string> {
    let episodes:string = '';
    const formData = new FormData();
    formData.append('webtoon_id', webtoon_id);
    const response = await fetch("/episode", {
        method: "POST",
        body: formData,
    });
    if (response.ok) {
        const data = await response.json();
        console.log(data);
        if (Array.isArray(data)) { // data가 배열인지 확인
            data.forEach((item: any) => {
                episodes += `
                <div class="col alert alert-success" style="width: 800px;">
                    <a href="https://comic.naver.com/webtoon/detail?titleId=${webtoon_id}&no=${item.id}" class="alert-link" target='_blank'>${item.title}</a>
                </div>`;
            });
        } else {
            alert("에피소드 정보를 불러오는데 실패했습니다.");
        }
    } else {
        alert("정보를 불러오는데 실패했습니다.");
    }
    return episodes;
}

getEpisode().then(result => {
  listElement.innerHTML = result;
});