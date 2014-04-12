Done, 4 points in 0 moves (best tile: 2).
Time elapsed: 0.75 seconds
+-----+-----+-----+
|     |     |   2 |
+-----+-----+-----+
|     |     |   2 |
+-----+-----+-----+
|     |     |     |
+-----+-----+-----+

Done, 26 points in 10 moves (best tile: 16).
Time elapsed: 5.88 seconds
+-----+-----+-----+
|   4 |  16 |   2 |
+-----+-----+-----+
|   2 |     |     |
+-----+-----+-----+
|   2 |     |     |
+-----+-----+-----+

Done, 46 points in 20 moves (best tile: 16).
Time elapsed: 7.76 seconds
+-----+-----+-----+
|   4 |  16 |   2 |
+-----+-----+-----+
|     |  16 |   2 |
+-----+-----+-----+
|     |   2 |   4 |
+-----+-----+-----+

Done, 66 points in 30 moves (best tile: 32).
Time elapsed: 9.49 seconds
+-----+-----+-----+
|   8 |     |     |
+-----+-----+-----+
|  16 |  32 |   2 |
+-----+-----+-----+
|   4 |   4 |     |
+-----+-----+-----+

Done, 88 points in 40 moves (best tile: 64).
Time elapsed: 10.41 seconds
+-----+-----+-----+
|   2 |   8 |   4 |
+-----+-----+-----+
|     |  64 |   4 |
+-----+-----+-----+
|     |   2 |   4 |
+-----+-----+-----+

Done, 114 points in 50 moves (best tile: 64).
Time elapsed: 11.23 seconds
+-----+-----+-----+
|   2 |  16 |   2 |
+-----+-----+-----+
|  64 |  16 |     |
+-----+-----+-----+
|   8 |   2 |   4 |
+-----+-----+-----+

Done, 134 points in 60 moves (best tile: 64).
Time elapsed: 11.81 seconds
+-----+-----+-----+
|   2 |   4 |   2 |
+-----+-----+-----+
|  64 |  32 |   8 |
+-----+-----+-----+
|   2 |   4 |  16 |
+-----+-----+-----+

         35325258 function calls (28388140 primitive calls) in 11.807 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000   11.807   11.807 2048.py:1(<module>)
        1    0.000    0.000    0.000    0.000 2048.py:102(generate_movements)
     5488    0.061    0.000    0.087    0.000 2048.py:108(move)
    38978    0.076    0.000   11.286    0.000 2048.py:129(get_copy)
     5428    0.011    0.000    0.011    0.000 2048.py:132(equal)
       60    0.000    0.000    0.000    0.000 2048.py:143(new_cell_value)
        1    0.000    0.000    0.000    0.000 2048.py:15(_GetchUnix)
        1    0.000    0.000    0.000    0.000 2048.py:16(__init__)
    32259    0.078    0.000    0.078    0.000 2048.py:173(heur_1)
 38073/61    0.193    0.000   11.802    0.193 2048.py:181(minimax)
        1    0.001    0.001   11.806   11.806 2048.py:226(AI)
        1    0.000    0.000    0.000    0.000 2048.py:30(_GetchWindows)
        1    0.000    0.000    0.000    0.000 2048.py:31(__init__)
        1    0.000    0.000    0.000    0.000 2048.py:38(Map)
        1    0.000    0.000    0.000    0.000 2048.py:43(__init__)
        1    0.000    0.000    0.000    0.000 2048.py:5(_Getch)
       62    0.000    0.000    0.001    0.000 2048.py:58(get_random_empty)
        1    0.000    0.000    0.000    0.000 2048.py:7(__init__)
    33610    0.012    0.000    0.012    0.000 2048.py:75(set_cell)
    38073    0.123    0.000    0.135    0.000 2048.py:78(get_empty_cells)
        7    0.000    0.000    0.000    0.000 2048.py:86(print_map)
   116984    0.025    0.000    0.025    0.000 2048.py:99(is_valid)
        1    0.000    0.000    0.000    0.000 __future__.py:48(<module>)
        1    0.000    0.000    0.000    0.000 __future__.py:74(_Feature)
        7    0.000    0.000    0.000    0.000 __future__.py:75(__init__)
5378964/38978    4.651    0.000   11.211    0.000 copy.py:145(deepcopy)
   560226    0.055    0.000    0.055    0.000 copy.py:198(_deepcopy_atomic)
1715032/194890    2.784    0.000    9.012    0.000 copy.py:226(_deepcopy_list)
77956/38978    0.264    0.000   10.764    0.000 copy.py:253(_deepcopy_dict)
  2392192    1.244    0.000    1.583    0.000 copy.py:267(_keep_alive)
    38978    0.104    0.000   11.100    0.000 copy.py:283(_deepcopy_inst)
        1    0.000    0.000    0.000    0.000 hashlib.py:55(<module>)
        6    0.000    0.000    0.000    0.000 hashlib.py:94(__get_openssl_constructor)
        1    0.000    0.000    0.000    0.000 random.py:100(seed)
       62    0.000    0.000    0.000    0.000 random.py:173(randrange)
       62    0.000    0.000    0.000    0.000 random.py:237(randint)
        1    0.000    0.000    0.001    0.001 random.py:40(<module>)
        1    0.000    0.000    0.000    0.000 random.py:651(WichmannHill)
        1    0.000    0.000    0.000    0.000 random.py:72(Random)
        1    0.000    0.000    0.000    0.000 random.py:801(SystemRandom)
        1    0.000    0.000    0.000    0.000 random.py:91(__init__)
        1    0.000    0.000    0.000    0.000 tty.py:1(<module>)
        1    0.000    0.000    0.000    0.000 {_hashlib.openssl_md5}
        1    0.000    0.000    0.000    0.000 {_hashlib.openssl_sha1}
        1    0.000    0.000    0.000    0.000 {_hashlib.openssl_sha224}
        1    0.000    0.000    0.000    0.000 {_hashlib.openssl_sha256}
        1    0.000    0.000    0.000    0.000 {_hashlib.openssl_sha384}
        1    0.000    0.000    0.000    0.000 {_hashlib.openssl_sha512}
        1    0.000    0.000    0.000    0.000 {binascii.hexlify}
        1    0.000    0.000    0.000    0.000 {function seed at 0x2744e60}
        6    0.000    0.000    0.000    0.000 {getattr}
        6    0.000    0.000    0.000    0.000 {globals}
   155912    0.118    0.000    0.118    0.000 {hasattr}
  9642100    0.529    0.000    0.529    0.000 {id}
        1    0.000    0.000    0.000    0.000 {math.exp}
        2    0.000    0.000    0.000    0.000 {math.log}
        1    0.000    0.000    0.000    0.000 {math.sqrt}
       63    0.000    0.000    0.000    0.000 {max}
  7163614    0.661    0.000    0.661    0.000 {method 'append' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
  7773939    0.779    0.000    0.779    0.000 {method 'get' of 'dict' objects}
    77956    0.013    0.000    0.013    0.000 {method 'iteritems' of 'dict' objects}
      122    0.000    0.000    0.000    0.000 {method 'random' of '_random.Random' objects}
    38978    0.021    0.000    0.021    0.000 {method 'update' of 'dict' objects}
        1    0.000    0.000    0.000    0.000 {min}
        1    0.000    0.000    0.000    0.000 {posix.urandom}
        4    0.000    0.000    0.000    0.000 {range}
        7    0.000    0.000    0.000    0.000 {round}
        8    0.000    0.000    0.000    0.000 {time.time}


