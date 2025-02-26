function loadNavbar():void {
    let login:string ='';

    const navbarHtml = `
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">HamToon</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarText" aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarText">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item">
                    <a class="nav-link ${login}" href="/">홈</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/mypage">마이페이지</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/login">로그인</a>
                </li>
                </ul>
            </div>
        </div>
    </nav>`;

    const navbarPlaceholder = document.getElementById('navbar-placeholder') as HTMLDivElement;
    navbarPlaceholder.innerHTML = navbarHtml;
}

export { loadNavbar };