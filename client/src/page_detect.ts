const title:string = document.title.split(',')[1];

function is_this(params:string):boolean{
    return title === params;
}

function is_main():boolean{
    return is_this('홈');
}

function is_mypage():boolean{
    return is_this('마이페이지');
}

function is_login():boolean{
    return is_this('로그인');
}

function is_signup():boolean{
    return is_this('회원가입');
}

export {is_main, is_mypage, is_login, is_signup, is_this};