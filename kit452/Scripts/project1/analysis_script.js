// analysis_script.js
document.addEventListener("DOMContentLoaded", function() {
    // URL에서 웹툰 제목 가져오기
    var urlParams = new URLSearchParams(window.location.search);
    var comicTitle = urlParams.get('title');

    // 웹툰 제목이 있는 경우 표시
    if (comicTitle) {
        document.getElementById("comicTitle").textContent = comicTitle;
    } else {
        document.getElementById("comicTitle").textContent = "웹툰 제목";
    }

    // 웹툰 제목 클릭 시 분석 페이지로 이동
    document.getElementById("comicTitle").addEventListener("click", function() {
        // 분석 페이지로 이동하는 URL 생성
        var analysisURL = "analysis.html?title=" + encodeURIComponent(comicTitle);
        window.location.href = analysisURL;
    });
});
