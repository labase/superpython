.. _Pybuilder: http://pybuilder.github.io/
.. _Google_Cloud: https://cloud.google.com/
.. _release1_1_2:

############################
Notas de Lançamento V. 1.1.2
############################

*SuperPython*

Milestone
=========

hidenseek - Suporte a importação cruzada

Aspectos do Lançamento
======================

Destaques dos Aspectos
**********************

Este ambiente permite rodar um game stand alone e criar módulos que não estão no menu. Agregando a lib do Phaser.

Aspecto #1
**********

Para rodar um game basta chamar <projeto>.is-by.us/code/_<modulo>. O submódulo *main.py* será importado.

Aspecto #2
**********

Para criar ou acessar um módulo fora do menu basta clicar a letra **O** no canto inferior direito do menu principal.

Aspecto #3
**********

A biblioteca Phaser está disponível baixada do CDN.

Melhoramentos
=============

Novo menu visual e gif de carregamento.

Melhoramento #1
***************

O novo menu visual é simétrico e suporta até cinquenta usuários.

Melhoramento #2
***************

Um gif animado com engrenagens rodando indica a carga do editor.

Consertos
=========

Ajuste da estrutura de configuração para facilitar os testes

Conserto #01
************

Adiciona o arquivo *vendor.py* para eliminar lib no import do bottle.


Questões e Problemas Conhecidos
===============================

1.  Ainda está congelado na versão antiga do Brython 3.0.2
#.  Aparece uma imagem espúria *em construção* quando roda o jogo *stand alone*.

Lançamentos Anteriores e Posteriores
====================================

Próximo Lançamento: A ser definido :ref:`Lançamento 1.1.3 <release1_1_2>`

Lançamento Anterior: Novembro 2015 :ref:`Lançamento 1.1.1 <release1_1_1>`

