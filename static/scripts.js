document.addEventListener("DOMContentLoaded", function() {
    // 웹툰 목록을 불러오는 함수 호출
    loadWebtoons();

    // 웹툰 추가 버튼에 클릭 이벤트 리스너 추가
    var addComicBtn = document.getElementById("addComicBtn");
    if (addComicBtn) {
        addComicBtn.addEventListener("click", function() {
            displayComicPopup();
        });
    } else {
        console.error("addComicBtn이 존재하지 않습니다.");
    }
});

// 웹툰 목록을 불러오는 함수
function loadWebtoons() {
    fetch('/webtoons')
        .then(response => response.json())
        .then(data => {
            // 가져온 데이터를 이용하여 웹툰 박스 생성
            data.forEach(webtoon => {
                createComicBox(webtoon.title, webtoon.id);
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// 웹툰 추가 팝업을 표시하는 함수
function displayComicPopup() {
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

        // 서버에 웹툰 추가 요청
        fetch('/new_webtoon', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ title: comicTitle, url: comicURL })
        })
        .then(response => response.json())
        .then(data => {
            // // 추가된 웹툰 박스 생성
            // createComicBox(comicTitle, data.id);

            // 페이지 새로고침
            location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
        });

        // 팝업 닫기
        document.body.removeChild(popupContainer);
    });

    // 취소 버튼에 클릭 이벤트 리스너 추가
    document.getElementById("cancelComicBtn").addEventListener("click", function() {
        // 팝업 닫기
        document.body.removeChild(popupContainer);
    });
}

// 웹툰 박스 생성 함수
function createComicBox(comicTitle, webtoonId) {
    // 웹툰 박스를 담을 div 요소 생성
    var comicBox = document.createElement("div");
    comicBox.classList.add("comic-box");

    // 해당 웹툰의 ID를 데이터 속성으로 추가
    comicBox.dataset.webtoonId = webtoonId;

    // 웹툰 제목을 표시하는 요소를 클릭 가능한 링크로 변경
    var titleLink = document.createElement("a");
    titleLink.textContent = comicTitle;
    titleLink.href = "#"; // 클릭 시 페이지 이동하지 않고 기본 동작 실행

    // 클릭 시 분석 페이지로 이동
    titleLink.addEventListener("click", function(event) {
        event.preventDefault(); // 기본 동작 취소
        
        // 웹툰 정보를 불러와서 분석 페이지로 이동
        fetch('/webtoon_one?title=' + encodeURIComponent(comicTitle))
            .then(response => response.json())
            .then(data => {
                // 분석 페이지로 이동하면서 데이터 전달
                window.location.href = "analysis?title=" + encodeURIComponent(comicTitle);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });

    // 삭제 버튼 생성
    var deleteButton = document.createElement("button");
    deleteButton.textContent = "삭제";
    deleteButton.classList.add("delete-btn");

    // 삭제 버튼에 클릭 이벤트 리스너 추가
    deleteButton.addEventListener("click", function() {
        // 해당 웹툰의 ID 가져오기
        var webtoonId = comicBox.dataset.webtoonId;
        
        // 서버에 삭제 요청 보내기
        fetch('/delete_webtoon', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: webtoonId })
        })
        .then(response => response.json())
        .then(data => {
            // 삭제 성공한 경우 해당 웹툰 박스 삭제
            if (data.success) {
                comicBox.parentNode.removeChild(comicBox);
            } else {
                console.log(data.message); // 실패한 경우 메시지 출력
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    // 웹툰 박스에 제목과 삭제 버튼 추가
    comicBox.appendChild(titleLink);
    comicBox.appendChild(deleteButton);

    // main 요소에 웹툰 박스 추가
    document.querySelector("main").appendChild(comicBox);
}
