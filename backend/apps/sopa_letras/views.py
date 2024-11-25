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

        # for fila, index in enumerate(word_search):

        #     print(fila, index)

        #     for columna, dato in enumerate(index):
        #         print(columna, dato)

        for word in words:
            # print(word[0].upper())

            upper_word = word.upper()

            print(upper_word, 'upper')

            for row, index in enumerate(word_search):

                if upper_word[0] in index:
                    print('existe')

                    position = [i for i, value in enumerate(index) if value == upper_word[0]]

                    print(position)

                    result.append(self.send(row, position, upper_word, index))

                    print(result, 'result')


                # print(letter, 'aaaaaaaaaa')
                break
            break

        # pprint.pprint(words)

        return 'aa'
    
    def send(self, row, position, word, index):
        
        print(row, position, word, index,'ppppppppppppppppppppppppppppppp')

        message = ''

        message = self.send_horizontal(index, word, row)

        print(message, 'mensaje')

        if message: 
            return message

        print('continua')

        # self.send_vertical(letter, word)
        # self.send_diagonal(letter, word)


    def send_horizontal(self, index, word, row):

        print('--------------------------')

        msg = 'la palabra {} existe en la fila {}'

        str_index = "".join(index)

        print(str_index)
        print(str_index[::-1])

        print(word)

        if word in str_index:
            print('existe --------------------------------')
            return msg.format(word, row)
        
        if word in str_index[::-1]:
            print('existe 2 --------------------------------')
            return msg.format(word, row)


        
        return None

        print(word)
        # print(r)

    def send_vertical():
        pass

    def send_diagonal():
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