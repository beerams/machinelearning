from IPython.display import display_markdown


def print_h4(s):
    print_md('#### ' + s)


def print_table(header, rows):
    md = ['|' + ' | '.join(header) + '|']
    for i, row in enumerate(rows):
        if i == 0:
            n_cols = len(row)
            md.append('|--'*n_cols + '|')
        md.append('| {} |'.format(' | '.join([str(cell) for cell in row])))
    display_markdown('\n'.join(md), raw=True)


def print_md(s):
    display_markdown(s, raw=True)
