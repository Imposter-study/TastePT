// server.js
console.log('Node.js 서버가 시작되었습니다.');

// 컨테이너가 계속 실행되도록 무한 대기
setInterval(() => {
  console.log('서버 실행 중... ' + new Date().toISOString());
}, 60000); // 1분마다 로그 출력