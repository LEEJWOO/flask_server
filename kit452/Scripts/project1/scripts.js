document.addEventListener("DOMContentLoaded", function() {
    // 웹툰 추가 버튼에 클릭 이벤트 리스너 추가
    document.getElementById("addComicBtn").addEventListener("click", function() {
        // 팝업을 표시하기 위한 div 요소 생성
        var popupContainer = document.createElement("div");
        popupContainer.classList.add("popup-container");

        // 팝업 내용을 담을 div 요소 생성
        var popupContent = document.createElement("div");
        popupContent.classList.add("popup-content");

        // 팝업 내용 구성
        popupContent.innerHTML = `
            <h2>웹툰 추가</h2>
            <label for="comicTitle">제목:</label>
            <input type="text" id="comicTitle" name="comicTitle" required><br><br>
            <label for="comicURL">URL:</label>
            <input type="url" id="comicURL" name="comicURL" required><br><br>
            <button id="submitComicBtn">추가</button>
            <button id="cancelComicBtn">취소</button>
        `;

        // 팝업에 내용 추가
        popupContainer.appendChild(popupContent);

        // body에 팝업 요소 추가
        document.body.appendChild(popupContainer);

        // 추가 버튼에 클릭 이벤트 리스너 추가
        document.getElementById("submitComicBtn").addEventListener("click", function() {
            // 입력된 웹툰 정보 가져오기
            var comicTitle = document.getElementById("comicTitle").value;
            var comicURL = document.getElementById("comicURL").value;

            // 박스 생성
            createComicBox(comicTitle);

            // 팝업 닫기
            document.body.removeChild(popupContainer);
        });

        // 취소 버튼에 클릭 이벤트 리스너 추가
        document.getElementById("cancelComicBtn").addEventListener("click", function() {
            // 팝업 닫기
            document.body.removeChild(popupContainer);
        });
    });

    // 웹툰 박스 생성 함수
    function createComicBox(comicTitle) {
        // 웹툰 박스를 담을 div 요소 생성
        var comicBox = document.createElement("div");
        comicBox.classList.add("comic-box");

        // 웹툰 제목을 표시하는 요소를 클릭 가능한 링크로 변경
        var titleLink = document.createElement("a");
        titleLink.textContent = comicTitle;
        titleLink.href = "analysis.html?title=" + encodeURIComponent(comicTitle);

        // 클릭 시 페이지 이동을 기본 동작으로 설정
        titleLink.addEventListener("click", function(event) {
            event.preventDefault(); // 기본 동작 취소
            // 분석 페이지로 이동
            window.location.href = titleLink.href;
        });

        // 삭제 버튼 생성
        var deleteButton = document.createElement("button");
        deleteButton.textContent = "삭제";
        deleteButton.classList.add("delete-btn");

        // 삭제 버튼에 클릭 이벤트 리스너 추가
        deleteButton.addEventListener("click", function() {
            // 해당 박스 삭제
            comicBox.parentNode.removeChild(comicBox);
        });

        // 웹툰 박스에 제목과 삭제 버튼 추가
        comicBox.appendChild(titleLink);
        comicBox.appendChild(deleteButton);

        // main 요소에 웹툰 박스 추가
        document.querySelector("main").appendChild(comicBox);
    }

});
