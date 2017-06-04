# Eleição 2017

Eleição de líder entre peers feito para disciplina de Redes de Computadores II

## Configuração
A rede deve ter 4 nodos, cada um deve ter um endereço IP diferente.
O endereço IP de cada nodo deve ser colocado na variavél(dicionário)  `NODES` dentro do arquivo `eleicao2017.py`, sendo as chaves do dicionário o id do nodo e o valor o seu IP e porta.
## Instalando dependências

```bash
 make install
```

## Rodando
Em cada um dos 4 nodos você rodar o seguinte comando:
``` python
python main.py id_node
```
O `id_node` variam de 0 a 3 e deve ser colocado de acordo com o IP do nodo.


