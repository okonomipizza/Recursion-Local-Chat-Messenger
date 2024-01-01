import socket
import sys

# TCP/IPソケットを作成
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server_address = '/socket_file'

#サーバに接続
print('connecting to {}'.format(server_address))
try:
    sock.connect(server_address)
except socket.error as err:
    print(err)
    sys.exit(1)

try:
    #ユーザーから入力を受けてサーバへ送信
    message = input("Input message: ")
    sock.sendall(message.encode())

    #サーバからの応答を2秒待つ
    sock.settimeout(2)

    #サーバから応答があれば、それを表示
    try:
        while True:
            data = sock.recv(32)
            data_str = data.decode('utf-8')

            if data:
                print('Server response: ' + data_str)
            else:
                break
    except(TimeoutError):
        print('Socket timeout, ending listening for server messages')

#通信終了時にはソケットを閉じる
finally:
    print('Closing socket')
    sock.close()



