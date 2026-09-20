import socket

HOST = '127.0.0.1'
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Сервер успешно запущен на http://{HOST}:{PORT}")

while True:
    client_socket, client_address = server_socket.accept()
    request_data = client_socket.recv(4096).decode('utf-8', errors='ignore')

    if not request_data:
        client_socket.close()
        continue


    lines = request_data.split('\r\n')
    request_line = lines[0]
    method, path, _ = request_line.split(' ')

    # Обработка POST-запроса от формы контактов
    if method == 'POST':
        body = request_data.split('\r\n\r\n')[-1]
        print(f"\n[POST ДАННЫЕ ОТ ПОЛЬЗОВАТЕЛЯ]: {body}")

        response_header = "HTTP/1.1 303 See Other\r\nLocation: /\r\n\r\n"
        client_socket.sendall(response_header.encode('utf-8'))
        client_socket.close()
        continue

    # Обработка GET-запросов

    if '.css' in path:
        try:

            local_path = path.lstrip('/')
            with open(local_path, 'r', encoding='utf-8') as file:
                css_content = file.read()

            response_header = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/css; charset=utf-8\r\n"
                f"Content-Length: {len(css_content.encode('utf-8'))}\r\n"
                "Connection: close\r\n\r\n"
            )
            response = response_header.encode('utf-8') + css_content.encode('utf-8')
        except FileNotFoundError:
            response = b"HTTP/1.1 404 Not Found\r\n\r\n"

    # На любые другие запросы возвращаем страницу контактов
    else:
        try:

            with open('src/templates/contacts.html', 'r', encoding='utf-8') as file:
                html_content = file.read()

            response_header = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
                "Connection: close\r\n\r\n"
            )
            response = response_header.encode('utf-8') + html_content.encode('utf-8')
        except FileNotFoundError:
            error_msg = "<h1>Ошибка: Файл contacts.html не найден</h1>"
            response = ("HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n" + error_msg).encode('utf-8')

    client_socket.sendall(response)
    client_socket.close()
