from typing import Optional


is_leaving = False
parent: Optional[object] = None
node: Optional[object] = None

loop = -1


while True:
    if is_leaving:
        assert parent is not None

        node = parent
        reveal_type(node)
        is_leaving = False

    else:
        loop += 1
        parent = object()
        is_leaving = True

    if loop >= 2:
        break
