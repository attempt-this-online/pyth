#!/usr/bin/python3
import pyth
import sys

# The idea here is to test each type as input to each function.
# num, float, str, list, tuple, set, dict

test_cases = [
    # Ideally, we want to have tests for every possible token. Please don't
    # move the tests around, they should be in the same order as in doc.txt

    # 0
    ('01', '0\n1\n'),
    ('0.1', '0\n0.1\n'),
    ('007', '0\n0\n7\n'),
    # 0123456789
    ('-1023 5123', '-4100'),
    # \n
    ('1\n1', '1\n1'),
    ('\np1', '10'),
    #
    ('1 1', '1'),
    ('1  1', '1'),
    # !
    ('!0', 'True'),
    ('!.0', 'True'),
    ('!"', 'True'),
    ('![', 'True'),
    ('!(', 'True'),
    ('!{', 'True'),
    ('!.d[', 'True'),
    ('!q1 0', 'True'),
    ('!>2 1', 'False'),
    ('!]0', 'False'),
    ('!.5', 'False'),
    ('!(1', 'False'),
    ('!"Hallo', 'False'),
    ('!{"Hallo', 'False'),
    ('!.d[,1 2', 'False'),
    # "
    ('"a', 'a\n'),
    ('"a"', 'a\n'),
    ('"\\', '\\\n'),
    ('"\\"', '"\n'),
    ('"\\""', '"\n'),
    ('"\\\\', '\\\n'),
    ('"\\\\\\"', '\\"\n'),
    ('"\n', '\n\n'),
    # #
    ('#1B1', '1\n1'),
    ('#1/1 0 2)2', '1\n2'),
    ('#/2-2Z~Z1', '1\n2'),
    # $
    # %
    ('%5 2', '1'),
    ('%6 3', '0'),
    ('%3U8', '[0, 3, 6]'),
    ('%2"YNeos', 'Yes'),
    ('%2(1 2 3 4', '(1, 3)'),
    ('%"i=%d"1', 'i=1'),
    ('%"%s=%d",\i1', 'i=1'),
    ('%"%0.2f".12345', '0.12'),
    # &
    ('&1 0', '0'),
    ('&!0!0', 'True'),
    ('&!1!0', 'False'),
    ('&0/1Z', '0'),
    ('&2 3', '3'),
    # '
    # (
    ('(', '()'),
    ('()', '()'),
    ('(1', '(1,)'),
    ('(1 2', '(1, 2)'),
    ('(1"abc"3)', "(1, 'abc', 3)"),
    # )
    ('(1)2', '(1,)\n2'),
    ('V3N)0', '0\n1\n2\n0'),
    ('FN"abc"N)0', 'a\nb\nc\n0'),
    ('#/1Z)1', '1'),
    ('c"a b")1', "['a', 'b']\n1"),
    # *
    ('*3 2', '6'),
    ('*3 .5', '1.5'),
    ('.R*.1.2 5', '0.02'),
    (r'*\x5', 'xxxxx'),
    ('*2"ab', 'abab'),
    ('*3]0', '[0, 0, 0]'),
    ('*[1 2 3)2', '[1, 2, 3, 1, 2, 3]'),
    ('*2,Z1', '(0, 1, 0, 1)'),
    ('*U3U2', '[(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]'),
    ('*"abc"U2',
        "[('a', 0), ('a', 1), ('b', 0), ('b', 1), ('c', 0), ('c', 1)]"),
    ('*"abc",0 1',
        "[('a', 0), ('a', 1), ('b', 0), ('b', 1), ('c', 0), ('c', 1)]"),
    ('*"ab""cd', "[('a', 'c'), ('a', 'd'), ('b', 'c'), ('b', 'd')]"),
    # +
    ('+4U3', '[4, 0, 1, 2]'),
    ('+U3U3', '[0, 1, 2, 0, 1, 2]'),
    ('+U3,01', '[0, 1, 2, (0, 1)]'),
    ('+1 10', '11'),
    ('+1.2 3', '4.2'),
    ('+,1 2,3 4', '(1, 2, 3, 4)'),
    ('+"12""41"', '1241'),
    ('+1(2', '(1, 2)'),
    ('+(1)2', '(1, 2)'),
    # ,
    (',"a"1', '(\'a\', 1)'),
    # -
    ('-5 2', '3'),
    ('-["a""b""a")"a"', '[\'b\']'),
    ('-3U5', '[]'),
    ('-(4 1 2 5 0)(1 2 1)', '(4, 5, 0)'),
    # .
    ('1.', '1.0'),
    ('.1', '0.1'),
    ('2.1', '2.1'),
    # /
    ('/3.1 .7', '4'),
    ('/312 105', '2'),
    ('/[1 2 1 3 1)1', '3'),
    ('/UT_1', '0'),
    ('/"abcda""a"', '2'),
    # :
    (':"abcde",0 3]"lol"', 'lolbclole'),
    (':"####$$$$"%2U8\\x', 'x#x#x$x$'),
    (':U10r4 7 8', '[0, 1, 2, 3, 8, 8, 8, 7, 8, 9]'),
    # ;
    ('chc"4 5";', '[\'4\']'),
    ('V2V2INN;', '1\n1\n'),
    # <
    ('<{1U2', 'True'),
    ('<G6', 'abcdef'),
    ('<1 2', 'True'),
    ('<"a""B"', 'False'),
    ('<[1 1 1)[0 2)', 'False'),
    # =
    ('=Z=Y2YZ', '2\n2'),
    ('*4=G3', '12'),
    ('=hZZ', '1'),
    ('=/T3T', '3'),
    ('JU2=XZJ3ZJ', '[3, 1]\n[3, 1]'),
    ('=,GHU2GH', '0\n1'),
    # >
    ('>{1U2', 'False'),
    ('>G20', 'uvwxyz'),
    ('>1 2', 'False'),
    ('>"a""B"', 'True'),
    ('>[1 1 1)[0 2)', 'True'),
    # ?
    ('?2 1 1', '2'),
    ('?2 0 1', '1'),
    ('?2 1 /1 0', '2'),
    # @
    ('@4 2', '2.0'),
    (' XH,01 2@HU2', '2'),
    ('@U3T', '1'),
    ('@[1 2 5)U4', '[1, 2]'),
    # A
    ('AGH,1 2', ''),
    ('AGH,1 2GH', '1\n2'),
    ('AGH,1 2HG', '2\n1'),
    ('Abd"ab"bd', 'a\nb'),
    ('ANNU2N', '1'),
    # B
    ('V4BN', '0'),
    ('#12B1', '12\n1'),
    # C
    ('C100', 'd'),
    ('C"d', '100'),
    ('C"abcd', '1633837924'),
    ('C,"ab""cd', '[(\'a\', \'c\'), (\'b\', \'d\')]'),
    ('C[U4r1 5r2 6', '[(0, 1, 2), (1, 2, 3), (2, 3, 4), (3, 4, 5)]'),
    # D
    ('DwR3w', '3'),
    ('DhdR*2dh7', '14'),
    # E
    ('IZ2)E3', '3'),
    ('V4N)E4', '0\n1\n2\n3\n4\n'),
    # F
    ('Fk3k', '0\n1\n2'),
    ('Fd<G3d', 'a\nb\nc'),
    ('rF,1 5', '[1, 2, 3, 4]'),
    ('^F[4 3 2 1', '4096'),
    # G
    ('G', 'abcdefghijklmnopqrstuvwxyz'),
    ('lG', '26'),
    # H
    ('H', '{}'),
    # I
    ('I3\n4', '4'),
    ('I0\n4', ''),
    # J
    ('J3J', '3'),
    # K
    ('KJ0KJ', '0\n0'),
    # L
    ('Lby5', '5'),
    ('L&b^2ytby3', '4'),
    # M
    ('M+GHg1\\1', '11'),
    ('hMU3', '[1, 2, 3]'),
    ('SM,"ba""31', "['ab', '13']"),
    ('>MC,U5_U5', '[False, False, False, True, True]'),
    ('xMC,U5r4T', '[4, 4, 4, 4, 12]'),
    # N
    ('N', '"'),
    # O
    ('O_1OT', '2'),
    # P
    ('PU3', '[0, 1]'),
    ('P"abc"', 'ab'),
    ('P2', '[2]'),
    ('P162', '[2, 3, 3, 3, 3]'),
    # Q
    # R
    ('DwR2w', '2'),
    # S
    ('S"bca', 'abc'),
    # T
    ('T', '10'),
    # U
    ('U"abc', '[0, 1, 2]'),
    ('U3', '[0, 1, 2]'),
    # V
    # W
    # X
    ('XUT5Z', '[0, 1, 2, 3, 4, 0, 6, 7, 8, 9]'),
    ('=YUT XY5Z', ''),
    ('=YUT XY15ZY', '[0, 1, 2, 3, 4, 0, 6, 7, 8, 9]'),
    ('X5UT5', '[0, 1, 2, 3, 4, 10, 6, 7, 8, 9]'),
    ('X"abc"1"d', 'adc'),
    ('X*2U5]1]2', '[0, 2, 2, 3, 4, 0, 2, 2, 3, 4]'),
    ('X"abcdef""ace""bdf', 'bbddff'),
    ('X"<></\\><>""</\\>', '><>\\/<><'),
    # Y
    # Z
    # [
    # \              (this text is here to prevent backslash line continuation)
    # ]
    # ^
    # _
    # `
    # a
    # b
    # c
    # d
    # e
    # f
    # g
    # h
    # i
    # j
    # k
    # l
    # m
    # n
    # o
    # p
    # q
    # r
    # s
    # t
    # u
    # v
    # w
    # x
    # y
    # z
    # {
    # |
    # }
    # ~
    # .a
    # .A
    # .B
    # .c
    ('.c0 0', '1'),
    ('.c0 3', '0'),
    ('.c3 0', '1'),
    ('.c5 12', '0'),
    ('.c17 12', '6188'),
    ('.c17 1', '17'),
    ('.c17 17', '1'),
    # .C
    # .d
    # .D
    # .e
    # .E
    # .f
    # .F
    # .h
    # .H
    # .j
    ('.j', '1j'),
    ('.j1', '(1+1j)'),
    ('.j3_2', '(3-2j)'),
    ('+.j2 1.j', '(2+2j)'),
    ('-.j4 2.j', '(4+1j)'),
    ('*.j3_2.j', '(2+3j)'),
    ('^.j1_1 2', '-2j'),
    ('_.j1_1', '(-1+1j)'),
    ('c.j2_6 2', '(1-3j)'),
    ('%.j5 3 2', '(1+1j)'),
    ('.a.j1 1', '1.4142135623730951'),
    ('C.j', '-1j'),
    ('P.j', '1.5707963267948966'),
    ('s.j.5.8', '0.5'),
    ('e.j.5.8', '0.8'),
    ('>.j.5.5.j', 'False'),
    ('<.j.5.5.j', 'True'),
    # .l
    # .m
    # .M
    # .n
    # .N
    # .O
    # .p
    # .P
    ('.P0 0', '1'),
    ('.P0 3', '0'),
    ('.P3 0', '1'),
    ('.P5 12', '0'),
    ('.P17 12', '2964061900800'),
    ('.P17 1', '17'),
    ('q.P17 17.!17', 'True'),
    # .q
    # .Q
    # .r
    # .R
    # .s
    # .S
    # .t
    # .u
    ('.u*NhYU5 1', '[1, 1, 2, 6, 24, 120]'),
    ('.ue*NN7', '[7, 9, 1]'),
    # .U
    # .V
    # .z
    # .^
    # .&
    # .|
    # .<
    # .>
    # ./
    ('./"abc"', "[['abc'], ['a', 'bc'], ['ab', 'c'], ['a', 'b', 'c']]"),
    ('./U4', '[[[0, 1, 2, 3]], [[0], [1, 2, 3]], [[0, 1], [2, 3]], '
     '[[0, 1, 2], [3]], [[0], [1], [2, 3]], [[0], [1, 2], [3]], '
     '[[0, 1], [2], [3]], [[0], [1], [2], [3]]]'),
    ('./3', '[(1, 1, 1), (1, 2), (3,)]'),
    ('./5', '[(1, 1, 1, 1, 1), (1, 1, 1, 2), (1, 1, 3), (1, 2, 2), '
     '(1, 4), (2, 3), (5,)]'),
    # .*
    ('J,1 5r.*J', '[1, 2, 3, 4]'),
    # .)
    # .(
    # .-
    # ._
    # .:
    ('.:U4 2', '[[0, 1], [1, 2], [2, 3]]\n'),
    ('.:"dcba"3', "['dcb', 'cba']\n"),
    ('.:4 2', '[[0, 1], [1, 2], [2, 3]]\n'),
    ('.:4 .5', '[[0, 1], [1, 2], [2, 3]]\n'),
    ('.:4U3', '[[0, 1, 2], [1, 2, 3]]\n'),
    ('.:3', '[[0], [1], [2], [0, 1], [1, 2], [0, 1, 2]]\n'),
    ('.:"abc")1', "['a', 'b', 'c', 'ab', 'bc', 'abc']\n1\n"),
    # .!
    ('.!5', '120'),
    ('.!0', '1'),
]


def test(pyth_code, expected_output, input_message=''):
    output, error = pyth.run_code(pyth_code, input_message)

    if input_message != '':
        if error:
            sys.exit("Error thrown by %s on input %s:\n%s" %
                     (pyth_code, input_message, error))
        if output != expected_output and output != expected_output + '\n':
            sys.exit("Bad output by %s on input %s."
                     "\nExpected: %r.\nReceived: %r" %
                     (pyth_code, input_message, expected_output, output))
    else:
        if error:
            sys.exit("Error thrown by %s:\n%s" %
                     (pyth_code, error))
        if output != expected_output and output != expected_output + '\n':
            sys.exit("Bad output by %s."
                     "\nExpected: %r.\nReceived: %r" %
                     (pyth_code, expected_output, output))

if __name__ == '__main__':
    for test_case in test_cases:
        test(*test_case)
    print("All " + str(len(test_cases)) + ' tests passed')
