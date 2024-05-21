def get_con(n):

    seq = [1]

    for x in range(n):
        # loops through conway seq to reach index u wanna get

        if seq == [1]:

            seq = [1, 1]

        else:

            n_seq = []

            cur_nb = seq[0]

            in_a_row = 1

            for index in range(1, len(seq)):

                if cur_nb == seq[index]:

                    in_a_row += 1

                else:

                    n_seq.append(in_a_row)

                    n_seq.append(cur_nb)

                    cur_nb = seq[index]

                    in_a_row = 1

            n_seq.append(in_a_row)

            n_seq.append(cur_nb)

            seq = n_seq

    return seq


for x in range(20):

    print(x, get_con(x))

print(len(get_con(55)))

    
