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
        data.forEach((item: any) => {
            episodes += `
            ${item.title}
            `;
        });
    } else {
        alert("정보를 불러오는데 실패했습니다.");
    }
    return episodes;
}

getEpisode().then(result => {
  listElement.innerHTML = result;
});