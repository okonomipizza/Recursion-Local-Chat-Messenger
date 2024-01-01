from faker import Faker
import socket
import os

#通信用にUNIXソケットを作成
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#次のファイルパスを利用してclient.pyのプロセスと通信する
server_address = '/socket_file'


#以前の接続が残っていれば、そのアドレスとのリンクを一度削除
try:
    os.unlink(server_address)
except FileExistsError:
    pass


print('Starting up on {}'.format(server_address))

# サーバアドレスにソケットを接続
sock.bind(server_address)

#clientからの接続要求があるまでソケットを待機させる
sock.listen(1)

while True:
    connection, client_address = sock.accept()

    try:
        print('connection from', client_address)

        while True:
            # ソケットから情報を受け取る
            data = connection.recv(16)
            data_str = data.decode('utf-8')
            print('Received ' + data_str)

            if data:
                #サンプルテキストを生成し、ソケットを通してクライアントへ返信
                fake = Faker()
                response = fake.text()
                print("Response is " + response)
                connection.sendall(response.encode())
                break
            else:
                print('no data from', client_address)
    #接続を閉じる
    finally:
        print("Closing current connection")
        connection.close()


