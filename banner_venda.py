from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle


class BannerVenda(GridLayout):

    def __init__(self, **kwargs):
        self.rows = 1
        super().__init__()

        with self.canvas:
            Color(rgb=(0, 0, 0, 0))
            self.rec = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.atualizar_rec, size=self.atualizar_rec)
        cliente = kwargs['cliente']
        foto_cliente = kwargs['foto_cliente']
        produto = kwargs['produto']
        foto_produto = kwargs['foto_produto']
        data = kwargs['data']
        preco = float(kwargs['preco'])
        quantidade = kwargs['quantidade']
        unidade = kwargs['unidade']


        esquerda = FloatLayout()
        esquerda_imagem = Image(pos_hint={'right': 1, 'top': 0.95}, size_hint=(1, 0.75),
                                source=f"icones/fotos_clientes/{foto_cliente}")
        esquerda_label = Label(text=cliente, pos_hint={'right': 1, 'top': 0.2}, size_hint=(1, 0.2))
        esquerda.add_widget(esquerda_imagem)
        esquerda.add_widget(esquerda_label)


        meio = FloatLayout()
        meio_imagem = Image(pos_hint={'right': 1, 'top': 0.95}, size_hint=(1, 0.75),
                                source=f"icones/fotos_produtos/{foto_produto}")
        meio_label = Label(text=produto, pos_hint={'right': 1, 'top': 0.2}, size_hint=(1, 0.2))
        meio.add_widget(meio_imagem)
        meio.add_widget(meio_label)


        direita = FloatLayout()
        direita_label_data = Label(text=f'Data: {data}', pos_hint={'right': 1, 'top': 0.9}, size_hint=(1, 0.33))
        direita_label_preco = Label(text=f'R${preco:.2f}', pos_hint={'right': 1, 'top': 0.65}, size_hint=(1, 0.33))
        direita_label_quantidade = Label(text=f'{quantidade} {unidade}', pos_hint={'right': 1, 'top': 0.4}, size_hint=(1, 0.33))
        direita.add_widget(direita_label_data)
        direita.add_widget(direita_label_preco)
        direita.add_widget(direita_label_quantidade)

        self.add_widget(esquerda)
        self.add_widget(meio)
        self.add_widget(direita)

    def atualizar_rec(self, *args):
        self.rec.pos = self.pos
        self.rec.size = self.size