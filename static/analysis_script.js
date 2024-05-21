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
        //페이지 이름 변경
        document.title = comicTitle + "분석 Page";
        //제목에 따른 문장 변경
        document.getElementById("comicTitle").textContent = comicTitle;
        document.getElementById("ratingAnalysisoverview").textContent = comicTitle + "에 대한 별점 분석 결과입니다.";
        document.getElementById("commentAnalysisoverview").textContent = comicTitle + "에 대한 댓글 분석 결과입니다.";
        document.getElementById("readerReactionAnalysisoverview").textContent = comicTitle + "에 대한 독자 반응 분석 결과입니다.";
  
        // 웹툰 정보를 가져오는 함수 호출
        fetchWebtoonData(comicTitle);
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
        window.print(); // 현재 페이지를 인쇄하기 위해 print() 함수를 사용합니다.
    }
  
    function getTitleIdFromUrl(url) {
        const urlObj = new URL(url);
        const params = new URLSearchParams(urlObj.search);
        return params.get('titleId');
    }

    // 웹툰 정보를 가져오는 함수 정의
    async function fetchWebtoonData(title) {
        const response = await fetch(`/webtoon_one?title=${encodeURIComponent(title)}`);
        const data = await response.json();
    
        // 가져온 데이터를 사용하여 페이지에 표시
        displayWebtoonData(data);
    
        // URL에서 titleId 추출
        const url = data.url;
        const titleId = getTitleIdFromUrl(url);
    
        // titleId와 에피소드 번호를 사용하여 감정 데이터 가져오기
        const startEpisode = Math.max(1, data.last_ep - 9); // 최소 에피소드 번호를 1로 설정
        const episodeNumbers = Array.from({length: Math.min(10, data.last_ep)}, (_, i) => startEpisode + i); // 총 에피소드 수를 고려
        const lineCounts = await fetchEpisodebyepisode(titleId, episodeNumbers);
        drawEpisodebyepisodeBarChart(episodeNumbers, lineCounts);
    
        // 최신 에피소드의 랜덤한 댓글 가져오기
        fetchBestCommentTextFile(titleId, data.last_ep);
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
                        min: 0, // 세로축의 최소값 설정
                        max: 10, // 세로축의 최대값 설정
                    }
                }
            },
        });
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
                        min: 0, // 세로축의 최소값 설정
                        max: 10, // 세로축의 최대값 설정
                    }
                }
            },
        });
    }

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
                      min: 0, // 세로축의 최소값 설정
                      max: 10, // 세로축의 최대값 설정
                  }
              }
            },
        });
    }
    //막대 그래프 그리기 함수
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

    //최신회차 별점
    function displayStars(star) {
        const stars = '★';
        document.getElementById('starRatingBox').innerHTML = stars + ' ' + star;
        document.getElementById('starRatingBox').style.color = 'red';
    }

    //피드백 보기
    function displayFeedback(text) {
        const feedbackBox = document.getElementById('feedbackBox');
        const htmlText = text.replace(/\\n/g, '\n');
        feedbackBox.innerHTML = marked.parse(htmlText);
    }

    //총평 보기
    function displayOverallSummary(text) {
        const overallSummaryBox = document.getElementById('overallSummaryBox');
        const htmlText = text.replace(/\\n/g, '\n');
        overallSummaryBox.innerHTML = marked.parse(htmlText);
    }
    
    function displayWebtoonData(data) {
        // 데이터 가져와서 원그래프 그리기
        const pieLabels = ['Positive', 'Negative'];
        const pieValues = [data.total_count.total_p, data.total_count.total_n];
        drawPieChart(pieLabels, pieValues);

        // 데이터 가져와서 선그래프 그리기 (최근 10화)
        const sortedStars10 = data.stars.star_list.sort((a, b) => b.episode - a.episode); // stars 배열을 역순으로 정렬
        const recentEpisodes10 = sortedStars10.slice(0, 10).reverse(); // 최근 10화만 선택
        const line10Labels = recentEpisodes10.map(episode => `Episode ${episode.episode}`);
        const line10Values = recentEpisodes10.map(episode => episode.star);
        draw10LineChart(line10Labels, line10Values);

        // 데이터 가져와서 선그래프 그리기 (최근 100화)
        const sortedStars100 = data.stars.star_list.sort((a, b) => b.episode - a.episode); // stars 배열을 역순으로 정렬
        const recentEpisodes100 = sortedStars100.slice(0, 100).reverse(); // 최근 100화만 선택
        const line100Labels = recentEpisodes100.map(episode => `Episode ${episode.episode}`);
        const line100Values = recentEpisodes100.map(episode => episode.star);
        draw100LineChart(line100Labels, line100Values);

        // 데이터 가져와서 전체 회차 선그래프 그리기
        const allEpisodes = data.stars.star_list.reverse(); // 전체 에피소드를 역순으로 정렬
        const allLabels = allEpisodes.map(episode => `Episode ${episode.episode}`);
        const allValues = allEpisodes.map(episode => episode.star);
        drawAllLineChart(allLabels, allValues);

        // 라벨을 원하는 순서로 정렬
        const labelOrder = ['작화', '스토리', '분량', '기타'];
        const sortedLabels = data.label.sort((a, b) => labelOrder.indexOf(a.label) - labelOrder.indexOf(b.label));
        //데이터 가져와서 카테고리 별 막대 그래프 그리기
        const barLabels = sortedLabels.map(label => label.label);
        const barValues = sortedLabels.map(label => label.positive_count);
        drawCategoriesBarChart(barLabels, barValues);

        displayStars(data.stars.star_list[data.stars.star_list.length - 1].star);
        
        displayFeedback(data.label_summary);
        displayOverallSummary(data.total_summary);         
    } 
});

async function fetchBestCommentTextFile(titleId, episodeNumber) {
    try {
        const response = await fetch(`/get_emotion_data/${titleId}/${episodeNumber}`);
        const text = await response.text();
        const lines = text.split('\n'); // 줄 단위로 분리
        const randomLine = lines[Math.floor(Math.random() * lines.length)]; // 랜덤한 줄 선택

        // 랜덤한 댓글을 웹 페이지에 표시
        document.getElementById('commentBox').textContent = randomLine;

        return randomLine;
    } catch (error) {
        console.error('Error fetching text file:', error);
    }
}

async function fetchEpisodebyepisode(titleId, episodeNumbers) {
    const lineCounts = [];
  
    for (const episodeNumber of episodeNumbers) {
      try {
        const response = await fetch(`/get_emotion_data/${titleId}/${episodeNumber}`);
        const data = await response.text();
        // 데이터 처리 로직
        const lineCount = data.split('\n').length; // 줄 수를 카운트함
        lineCounts.push(lineCount);
      } catch (error) {
        console.error(`에피소드 ${episodeNumber}에 대한 TXT 데이터를 가져오는 중 오류 발생:`, error);
      }
    }
  
    return lineCounts;
}
 
/* 분석요약 그래프
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
});*/

/* 최근 10회차 그래프
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
});*/

/* 최근 100회차 그래프
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
});*/

/* 전체회차 그래프
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
});*/

/* 카테고리
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
});*/

/* 회차별
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
});*/

/* 가장 최신화 별점
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
*/

/* 가장 최신화 베스트 댓글
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

displayBestComment();*/

/* 피드백
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
*/

/* 총평
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

displayOverallSummary();*/
