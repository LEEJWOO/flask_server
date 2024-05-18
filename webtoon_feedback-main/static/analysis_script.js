/*static/analysis_script.js*/

document.addEventListener("DOMContentLoaded", function() {
  // 홈 버튼에 클릭 이벤트 리스너 추가
  document.getElementById("homeBtn").addEventListener("click", function() {
      // index.html로 이동
      window.location.href = "/";
  });

  // URL에서 웹툰 제목 가져오기
  var urlParams = new URLSearchParams(window.location.search);
  var comicTitle = urlParams.get('title');

  // 웹툰 제목이 있는 경우 표시
  if (comicTitle) {
      document.getElementById("comicTitle").textContent = comicTitle;
      document.getElementById("ratingAnalysisoverview").textContent = comicTitle + "에 대한 별점 분석 결과입니다.";
      document.getElementById("commentAnalysisoverview").textContent = comicTitle + "에 대한 댓글 분석 결과입니다.";
      document.getElementById("readerReactionAnalysisoverview").textContent = comicTitle + "에 대한 독자 반응 분석 결과입니다.";
  } else {
      document.getElementById("comicTitle").textContent = "현재 웹툰";
  }

  // 웹툰 제목 클릭 시 분석 페이지로 이동
  document.getElementById("comicTitle").addEventListener("click", function() {
      // 분석 페이지로 이동하는 URL 생성
      var analysisURL = "analysis?title=" + encodeURIComponent(comicTitle);
      window.location.href = analysisURL;
  });

  // PDF로 저장 버튼에 클릭 이벤트 리스너 추가
  document.getElementById("pdfBtn").addEventListener("click", function() {
      saveAsPDF(); // PDF로 저장 함수 호출
  });

  // PDF로 저장하는 함수 정의
  function saveAsPDF() {
      // 현재 페이지를 PDF로 저장하는 코드를 추가
      // 이 코드는 각 브라우저에서 다를 수 있습니다.
      // 여기서는 간단한 예시를 들겠습니다.
      window.print(); // 현재 페이지를 인쇄하기 위해 print() 함수를 사용합니다.
  }
});

// 분석요약 그래프
async function fetchCSVData() {
  try {
      const response = await fetch('static/analysis_summary_data.CSV');
      const data = await response.text();
      // 데이터 처리 로직
      const rows = data.split('\n');
      const labels = [];
      const values = [];
      for (const row of rows) {
          const [label, value] = row.split(',');
          labels.push(label);
          values.push(parseInt(value));
      }
      return { labels, values };
  } catch (error) {
      console.error('Error fetching CSV data:', error);
  }
}

// 원그래프 그리기 함수
function drawPieChart(labels, values) {
  const ctx = document.getElementById('commentChart').getContext('2d');
  new Chart(ctx, {
      type: 'pie',
      data: {
          labels,
          datasets: [{
              data: values,
              backgroundColor: ['#36A2EB', '#FF6384'] // Customize colors as needed
          }],
      },
      options: {
          responsive: true,
          maintainAspectRatio: false,
      },
  });
}

// 데이터 가져와서 원그래프 그리기
fetchCSVData().then(({ labels, values }) => {
  drawPieChart(labels, values);
});

// 최근 10회차 그래프
async function fetchRecent10Rows() {
  try {
      const response = await fetch('static/star_data.csv');
      const data = await response.text();
      // 데이터 처리 로직
      const rows = data.split('\n').slice(-10); // 마지막 10줄만 가져옴
      const labels = [];
      const values = [];
      for (const row of rows) {
          const [label, value] = row.split(',');
          labels.push(label);
          values.push(parseInt(value));
      }
      return { labels, values };
  } catch (error) {
      console.error('Error fetching CSV data:', error);
  }
}

// 선그래프 그리기 함수
function draw10LineChart(labels, values) {
  const ctx = document.getElementById('recent10EpisodesGraphCanvas').getContext('2d');
  new Chart(ctx, {
      type: 'line',
      data: {
          labels,
          datasets: [{
              label: '별점', // 데이터셋 레이블을 '별점'으로 설정
              data: values,
              fill: false,
              borderColor: '#FF6384',
              tension: 0.1
          }],
      },
      options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
              y: {
                  min: 1, // 세로축의 최소값 설정
                  max: 10, // 세로축의 최대값 설정
              }
          }
      },
  });
}

// 데이터 가져와서 선그래프 그리기
fetchRecent10Rows().then(({ labels, values }) => {
  draw10LineChart(labels, values);
});

// 최근 100회차 그래프
// CSV 파일에서 데이터를 가져오는 함수
async function fetchRecent100Rows() {
  try {
      const response = await fetch('static/star_data.csv');
      const data = await response.text();
      // 데이터 처리 로직
      const rows = data.split('\n').slice(-100); // 마지막 100줄만 가져옴
      const labels = [];
      const values = [];
      for (const row of rows) {
          const [label, value] = row.split(',');
          labels.push(label);
          values.push(parseFloat(value));
      }
      return { labels, values };
  } catch (error) {
      console.error('Error fetching CSV data:', error);
  }
}

function draw100LineChart(labels, values) {
  const ctx = document.getElementById('recent100EpisodesGraphCanvas').getContext('2d');
  new Chart(ctx, {
      type: 'line',
      data: {
          labels,
          datasets: [{
              label: '별점', // 데이터셋 레이블을 '별점'으로 설정
              data: values,
              fill: false,
              borderColor: '#FF6384',
              tension: 0.1
          }],
      },
      options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
              y: {
                  min: 1, // 세로축의 최소값 설정
                  max: 10, // 세로축의 최대값 설정
              }
          }
      },
  });
}

// 데이터 가져와서 선그래프 그리기
fetchRecent100Rows().then(({ labels, values }) => {
  draw100LineChart(labels, values);
});

// 전체회차 그래프
// CSV 파일에서 데이터를 가져오는 함수
async function fetchAllRows() {
  try {
      const response = await fetch('static/star_data.csv');
      const data = await response.text();
      // 데이터 처리 로직
      const rows = data.split('\n'); // 모든 줄을 가져옴
      const labels = [];
      const values = [];
      for (const row of rows) {
          const [label, value] = row.split(',');
          labels.push(label);
          values.push(parseFloat(value));
      }
      return { labels, values };
  } catch (error) {
      console.error('Error fetching CSV data:', error);
  }
}

// 선그래프 그리기 함수
function drawAllLineChart(labels, values) {
  const ctx = document.getElementById('overallEpisodesGraphCanvas').getContext('2d');
  new Chart(ctx, {
      type: 'line',
      data: {
          labels,
          datasets: [{
              label: '별점', // 데이터셋 레이블을 '별점'으로 설정
              data: values,
              fill: false,
              borderColor: '#FF6384',
              tension: 0.1
          }],
      },
      options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
                min: 1, // 세로축의 최소값 설정
                max: 10, // 세로축의 최대값 설정
            }
        }
      },
  });
}

// 데이터 가져와서 선그래프 그리기
fetchAllRows().then(({ labels, values }) => {
  drawAllLineChart(labels, values);
});

// 카테고리
// CSV 파일에서 데이터를 가져오는 함수
async function fetchCategories() {
  try {
      const response = await fetch('static/categories_data.CSV');
      const data = await response.text();
      // 데이터 처리 로직
      const rows = data.split('\n'); // 모든 줄을 가져옴
      const labels = [];
      const values = [];
      for (const row of rows) {
          const [label, value] = row.split(',');
          labels.push(label);
          values.push(parseFloat(value));
      }
      return { labels, values };
  } catch (error) {
      console.error('Error fetching CSV data:', error);
  }
}

function drawCategoriesBarChart(labels, values) {
  const ctx = document.getElementById('categoriesGraphCanvas').getContext('2d');
  new Chart(ctx, {
      type: 'bar',
      data: {
          labels,
          datasets: [{
              label: '긍정',
              data: values,
              backgroundColor: '#36A2EB', // 모든 막대의 색깔 설정
              borderColor: '#36A2EB',
              borderWidth: 1
          }],
      },
      options: {
          responsive: true,
          maintainAspectRatio: false,
      },
  });
}

fetchCategories().then(({ labels, values }) => {
  drawCategoriesBarChart(labels, values);
});

// 회차별
async function fetchEpisodebyepisode() {
  try {
      const response = await fetch('static/episodebyepisode_data.CSV');
      const data = await response.text();
      // 데이터 처리 로직
      const rows = data.split('\n'); // 모든 줄을 가져옴
      const labels = [];
      const values = [];
      for (const row of rows) {
          const [label, value] = row.split(',');
          labels.push(label);
          values.push(parseFloat(value));
      }
      return { labels, values };
  } catch (error) {
      console.error('Error fetching CSV data:', error);
  }
}

function drawEpisodebyepisodeBarChart(labels, values) {
  const ctx = document.getElementById('episodeByEpisodeGraphCanvas').getContext('2d');
  new Chart(ctx, {
      type: 'bar',
      data: {
          labels,
          datasets: [{
              label: '긍정',
              data: values,
              backgroundColor: '#36A2EB', // 모든 막대의 색깔 설정
              borderColor: '#36A2EB',
              borderWidth: 1
          }],
      },
      options: {
          responsive: true,
          maintainAspectRatio: false,
      },
  });
}

fetchEpisodebyepisode().then(({ labels, values }) => {
  drawEpisodebyepisodeBarChart(labels, values);
});

// 가장 최신화 별점
async function fetchLastRow() {
  try {
      const response = await fetch('static/star_data.csv');
      const data = await response.text();
      const rows = data.split('\n');
      const lastRow = rows[rows.length - 1];
      const value = lastRow.split(',')[1];
      return parseFloat(value);
  } catch (error) {
      console.error('Error fetching CSV data:', error);
  }
}

function displayStars() {
  fetchLastRow().then(value => {
      const stars = '★';
      document.getElementById('starRatingBox').innerHTML = stars + ' ' + value.toFixed(1);
      document.getElementById('starRatingBox').style.color = 'red';
  });
}

displayStars();

//// 가장 최신화 베스트 댓글
async function fetchBestCommentTextFile(url) {
  try {
      const response = await fetch(url);
      return await response.text();
  } catch (error) {
      console.error('Error fetching text file:', error);
  }
}

function displayBestComment() {
  fetchBestCommentTextFile('static/best_comment.txt').then(text => {
      document.getElementById('commentBox').textContent = text;
  });
}

displayBestComment();

// 피드백
async function fetchfeedbackTextFile(url) {
  try {
      const response = await fetch(url);
      return await response.text();
  } catch (error) {
      console.error('Error fetching text file:', error);
  }
}

function displayFeedback() {
  fetchfeedbackTextFile('static/comment_feedback.txt').then(text => {
      document.getElementById('feedbackBox').textContent = text;
  });
}

displayFeedback();

// 총평
async function fetchoverallsummaryTextFile(url) {
  try {
      const response = await fetch(url);
      return await response.text();
  } catch (error) {
      console.error('Error fetching text file:', error);
  }
}

function displayOverallSummary() {
  fetchoverallsummaryTextFile('static/comment_overallsummary.txt').then(text => {
      document.getElementById('overallSummaryBox').textContent = text;
  });
}

displayOverallSummary();
