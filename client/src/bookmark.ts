const webtoon_id = location.href.split("/")[4];
const bookmark_btn = document.getElementById("bookmark-btn") as HTMLButtonElement;
console.log(webtoon_id);

bookmark_btn.addEventListener("click", async () => {
    const formData = new FormData();
    formData.append('webtoon_id', webtoon_id);
    const response = await fetch("/add_bookmark", {
        method: "POST",
        body: formData,
    });
    if (response.ok) {
        const responseText = await response.text();
        if (responseText === "added") {
            alert("북마크에 추가되었습니다.");
        } else {
            alert("북마크에서 제거되었습니다.");
        }
    } else {
        const responseText = await response.text();
        alert(`북마크에 실패했습니다. ${responseText}`);
    }
});
