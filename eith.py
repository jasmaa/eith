from interpreter import Interpreter


if __name__ == '__main__':
    with open('samples/add.eith', 'r+') as f:
        interp = Interpreter(f)
        while interp.has_more:
            interp.step()
        f.seek(0)
        f.write('\n'.join(interp.raw_lines)+'\n')
