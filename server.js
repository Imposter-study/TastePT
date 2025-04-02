const roomId = "{{ room_id }}"; 
const socket = new WebSocket(`ws://localhost:8000/ws/chat/${roomId}/`);

socket.onopen = function(event) {
    console.log("WebSocket Connected");
};

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log("Received message:", data.message);
    document.getElementById("chat-box").innerHTML += `<p>${data.user}: ${data.message}</p>`;
};

socket.onerror = function(event) {
    console.error("WebSocket Error", event);
};

socket.onclose = function(event) {
    console.log("WebSocket Disconnected");
};

document.getElementById("send-button").onclick = function() {
    const messageInput = document.getElementById("message-input");
    const message = messageInput.value;
    socket.send(JSON.stringify({'message': message}));
    messageInput.value = "";
};
