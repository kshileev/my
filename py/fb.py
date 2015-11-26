# 'a' => 0
# 'b' => 1
# ...
# 'z' => 25
#                    / "aba" 0, 1, 0
# "aba" => [0, 1, 0]
#                    \ "ak" 0, 10
#
# [0, 1, 0] => 2
# 
# [1, 1, 1, 1] => 5
# b b b b
# l b b 
# b l b
# b b l
# l l


# enc is an array of digits between 0..9 and can by empty
def ways(enc):
    if not enc:
        return 1
    
    n_comb = 1
    first = enc[0]

    if len(enc) > 1:
        second = enc[1] if len(enc) >1 else 0
        combined = 10*first + second
        if first != 0 and combined < 26:
            n_comb += 1

    if len(enc) > 1:
        n_comb += ways(enc[1:])
    
    return n_comb

