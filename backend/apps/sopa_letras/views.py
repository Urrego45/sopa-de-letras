from rest_framework import generics

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
import re

import pprint

class pruebaApi(APIView):    
    def post (self, request):

        letters, words = self.format_letter_words(request.data.get('letters'), request.data.get('words'))

        word_search = [letters[i:i+14] for i in range(0, len(letters), 14)]

        result = self.send_words(word_search, words)

        return Response([words, word_search], status=status.HTTP_200_OK)

    def format_letter_words(self, letter, words):

        letters_array = list(re.sub(r'[^a-zA-Z]', '', letter).upper())
        words_array = [word.lower() for word in re.findall(r'\b[a-zA-Z]+\b', words)]

        if len(letters_array) is not 196:
            raise ValidationError({'message': f'la cantidad de letras debe ser igual a 196 caracteres. letras actuales: {len(letters_array)}'})

        return letters_array, words_array
    
    def send_words(self, word_search, words):

        result = []
        pprint.pprint(word_search)
        pprint.pprint(word_search[1][0])

        for word in words:

            upper_word = word.upper()

            print(upper_word, 'upper')

            for row, index in enumerate(word_search):

                if upper_word[0] in index:
                    print('existe')

                    position = [i for i, value in enumerate(index) if value == upper_word[0]]

                    print(position)

                    result.append(self.send(row, position, upper_word, index, word_search))

                    print(result, 'result')


                # print(letter, 'aaaaaaaaaa')
                break
            break

        # pprint.pprint(words)

        return 'aa'
    
    def send(self, row, position, word, index, word_search):

        message = ''

        message = self.send_horizontal(index, word, row)

        if message: 
            return message

        print('continua')

        message = self.send_vertical(index, word, row, position, word_search)

        print(message)

        if message:
            return message

        # self.send_diagonal(letter, word)


    def send_horizontal(self, index, word, row):

        msg = 'la palabra {} existe en la fila {}'

        str_index = "".join(index)

        if word in str_index:
            return msg.format(word, row)
        
        if word in str_index[::-1]:
            return msg.format(word, row)
        
        return None

    def send_vertical(self, index, word, row, position, word_search):
        
        print(index, word, row, position)
        print(len(word))

        print(row - len(word))

        a = ''
        msg = 'Horizontal: la palabra {} existe desde la fila {} hasta la fila {}'

        if (row + len(word)) <= 13:

            print('dentro')

            print(word_search[0][0])
            print(word_search[1][0])
            print(word_search[2][0])
            print(word_search[3][0])

            for i, value in enumerate(word):

                if value is not word_search[i][row]:
                    break

                a += value


                print(i, value)

            print(a, word, 'llllll')
            print(a == word, 'llllll')
            print(word is a, 'llllll')

            if word == a:
                print('si es')
                return msg.format(word, row, row + len(word))

            print(a, 'aaaaaaaaaaaaa')
        
        return None

    def send_diagonal(self, index, word, row, position, word_search):
        pass


# o MANATI
# o PERRO -
# o GATO -
# o CONEJO
# o TIBURON
# o ELEFANTE
# o ALCON
# o SERPIENTE -
# o JAGUAR
# o CANGURO
# o LOBO -
# o MONO
# o NUTRIA
# o LEON
# o LORO
# o TORO
# o ORUGA


# N,D,E,K,I,C,A,N,G,U,R,O,G,E,
# S,X,R,Y,K,V,I,I,Q,G,W,Q,O,D,
# J,A,G,U,A,R,Z,W,B,N,K,O,U,A,
# M,L,E,L,E,F,A,N,T,E,H,O,G,W,
# L,O,B,O,N,U,T,R,I,A,O,U,S,U,
# W,W,O,S,O,G,A,T,O,V,R,T,M,O,
# H,L,Z,N,C,T,Y,Z,E,O,X,A,U,R,
# C,E,C,Y,T,I,B,U,R,O,N,S,R,O,
# C,O,N,E,J,O,Y,U,S,M,R,S,H,T,
# Y,N,I,F,E,F,P,T,E,Z,O,O,S,F,
# O,S,S,E,R,P,I,E,N,T,E,F,L,G,
# P,P,V,D,D,X,U,F,A,L,C,O,N,Y,
# M,O,N,O,C,U,Q,W,M,A,N,A,T,I,
# N,N,X,H,E,B,P,M,U,P,E,R,R,O