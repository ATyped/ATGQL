__all__ = ['promise_for_object']

import asyncio
from typing import TypeVar

from atgql.pyutils.obj_map import ObjMap
from atgql.shims import Promise

T = TypeVar('T')


def promise_for_object(obj: ObjMap[Promise[T]]) -> Promise[ObjMap[T]]:
    async def transformer() -> ObjMap[T]:
        return dict(zip(obj.keys(), await asyncio.gather(*obj.values())))

    return transformer()
