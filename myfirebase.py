import requests
from kivy.app import App


class MyFireBase():
    API_KEY = 'AIzaSyBPHMjjsvCSXbhvnHiYyfupJJ27oTF7kNE'

    def criar_conta_usuario(self, email, senha):
        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.API_KEY}"
        info = {"email": email,
                "password": senha,
                "returnSecureToken": True}
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()
        print(requisicao_dic)
        if requisicao.ok:
            print('USUARIO CRIADO')
            #requisicao_dic['idToken'] -> autenticação
            #requisicao_dic['refreshToken'] ->  token que mantém o usuario logado
            #requisicao_dic['LocalId'] -> id do usuario do banco de dados

            meu_aplicativo = App.get_running_app()

            refresh_token = requisicao_dic['refreshToken']
            local_id = requisicao_dic['localId']
            id_token = requisicao_dic['idToken']

            meu_aplicativo.local_id = local_id
            meu_aplicativo.id_token = id_token
            with open("refresh_token.txt", 'w') as arquivo:
                arquivo.write(refresh_token)
            req_id = requests.get(f"https://aplicativovendashash-88e7c-default-rtdb.firebaseio.com/proximo_id_vendedor.json?auth={meu_aplicativo.id_token}")
            id_vendedor = req_id.json()
            link = f'https://aplicativovendashash-88e7c-default-rtdb.firebaseio.com/{local_id}.json?auth={meu_aplicativo.id_token}'
            info_usuario = f'{{"avatar": "foto1.png", "equipe": "", "total_vendas": "0", "vendas": "", "id_vendedor": "{id_vendedor}"}}'
            requisicao_usuario = requests.patch(link, data=info_usuario)

            #atualizar o prox_id_vendedor
            proximo_id_vendedor = int(id_vendedor) + 1
            info_id_vendedor = f'{{"proximo_id_vendedor": "{proximo_id_vendedor}"}}'
            requests.patch(f'https://aplicativovendashash-88e7c-default-rtdb.firebaseio.com/.json?auth={meu_aplicativo.id_token}', data=info_id_vendedor)
            meu_aplicativo.mudar_tela('homepage')
            meu_aplicativo.carregar_info_usuario()


        else:
            mensagem_error = requisicao_dic['error']['message']
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids["loginpage"]
            pagina_login.ids['mensagem_login'].text = mensagem_error
            pagina_login.ids['mensagem_login'].color = (1, 0, 0, 1)

        pass

    def fazer_login_usuario(self, email, senha):
        link = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.API_KEY}'
        info = {"email": email,
                "password": senha,
                "returnSecureToken": True}
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()
        print(requisicao_dic)
        if requisicao.ok:
            # requisicao_dic['idToken'] -> autenticação
            # requisicao_dic['refreshToken'] ->  token que mantém o usuario logado
            # requisicao_dic['LocalId'] -> id do usuario do banco de dados

            meu_aplicativo = App.get_running_app()

            refresh_token = requisicao_dic['refreshToken']
            local_id = requisicao_dic['localId']
            id_token = requisicao_dic['idToken']

            meu_aplicativo.local_id = local_id
            meu_aplicativo.id_token = id_token
            with open("refresh_token.txt", 'w') as arquivo:
                arquivo.write(refresh_token)
            meu_aplicativo.mudar_tela('homepage')
            meu_aplicativo.carregar_info_usuario()


        else:
            mensagem_error = requisicao_dic['error']['message']
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids["loginpage"]
            pagina_login.ids['mensagem_login'].text = mensagem_error
            pagina_login.ids['mensagem_login'].color = (1, 0, 0, 1)

        pass

        pass


    def trocar_token(self, refresh_token):
        link = f'https://securetoken.googleapis.com/v1/token?key={self.API_KEY}'
        info = {"grant_type": "refresh_token",
                "refresh_token": refresh_token}
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()
        local_id = requisicao_dic['user_id']
        id_token = requisicao_dic['id_token']
        return local_id, id_token