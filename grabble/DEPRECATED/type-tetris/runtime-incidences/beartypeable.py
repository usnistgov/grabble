from beartype import beartype
from beartype import typing as bt
from beartype.door import TypeHint as TH
from beartype.door import UnionTypeHint, is_bearable
from abc import abstractmethod
import types

CT = bt.TypeVar("ClassType")


@bt.runtime_checkable
class BearTyped(bt.Protocol, bt.Generic[CT]):
    @classmethod
    @abstractmethod
    def __beartype__(cls: bt.Type[CT]) -> TH | bt.Sequence[TH]:
        ...


def beartypeable(compiletime=None):
    """nasty monkey-patching, do not use"""

    def decorator(myclass: bt.Type[CT]) -> BearTyped[CT]:
        @classmethod
        def __beartype__(
            cls: bt.Type[CT], compiletime: bt.Optional[TH] = compiletime
        ) -> TH:
            """Default janky behavior"""
            if compiletime and isinstance(cls, type):
                return compiletime
            else:
                return TH(cls)

        if not hasattr(myclass, "__beartype__"):
            setattr(myclass, "__beartype__", __beartype__)
        return myclass

    return decorator


def wrapped_is_bearable(  # forgive me, for I have copy-pasted
    # Mandatory flexible parameters.
    obj: object,
    hint,
):
    print("\n--CALLING WRAPPER--\n\n")
    if TH(hint) <= TH(BearTyped):
        myhint = hint.__beartype__()
        print(f"my hint says {hint}, but really that means a: \n\t{myhint}")
    else:
        myhint = TH(hint)
    if isinstance(obj, BearTyped):
        # forgive the use of isinstance
        print(f"\n\n I see it now!\n This hint is no mere {type(obj)}")
        mybeartype = obj.__beartype__()
        print(f"but a blessed {mybeartype}!\n My third eye has opened!\n\n")

        # oh look more isinstance
        if isinstance(myhint, UnionTypeHint):  # optimizeable overhead
            print(f"checking divergent timelines...{mybeartype.hint}")
            if mybeartype in myhint:  # verbatim matches one branch
                return True
            else:
                possibles = [wrapped_is_bearable(obj, t.hint) for t in myhint]
                # going recursive, see if any won
                return any(possibles)

        # so this is an ugly hack approximating prod type
        if myhint <= TH(tuple):
            print(f"checking convergent timelines...{mybeartype.hint}")
            if mybeartype <= TH(tuple):  # really should be...
                # well, except multiple inheritance
                # ok, and protocol overlapping... 0_o

                requirements = [
                    wrapped_is_bearable(x.hint, t.hint)
                    for x, t in zip(mybeartype, myhint)
                ]
            else:
                requirements = [
                    wrapped_is_bearable(mybeartype.hint, t.hint) for t in myhint
                ]
            print(
                "\nthese succeeded:\n\t ", list(zip(mybeartype, myhint, requirements))
            )
            return all(requirements)
        else:
            print("currently on the one true timeline")
            return myhint >= mybeartype

    else:
        print(f"Oh, this \n\t{obj}\n is a boring _normal_ thing...")
        return myhint.is_bearable(obj)


if __name__ == "__main__":

    # @beartypeable
    # class Fake(bt.NamedTuple):
    #     name: str
    #     kind: str
    #     velocity: float

    # fake_data = ("n1", "bob", 2.3)
    # fake: BearTyped = Fake(*fake_data)
    # FakeLike = bt.Tuple[str, str, float]  # let the shennanigans commence

    # print(
    #     "\nbaselines\n",
    #     TH(bt.Tuple[str, str, float]).is_bearable(fake),  # works, Tuple >= NamedTuple
    #     TH(Fake).is_bearable((fake_data)),  # Doesn't, NamedTuple <= Tuple
    #     TH(Fake) <= TH(FakeLike),  # works, Fake is a specialization of FakeLike
    #     "\n\nshennanigans\n",
    #     TH(bt.Tuple[str, str, float]) >= Fake.__beartype__(),  # should work, right?
    #     TH(bt.Tuple[str, str, float]) <= Fake.__beartype__(),
    #     TH(BearTyped).is_bearable(fake),
    #     fake.__beartype__() is TH(Fake),
    #     Fake.__beartype__() is TH(Fake),
    # )
    # class FakeID:
    #     """this is annoying boilerplate for BearSumType(?), since
    #     Enum's are evil. We must do better! ('cause this is garbage lol)
    #     """

    #     def __new__(cls, x: bt.Union[int, str]):
    #         instance = super().__new__(cls, x)
    #         return instances

    #     @classmethod
    #     def __beartype__(cls):
    #         return TH(bt.Union[int, str]) if isinstance(cls, type) else TH(type(cls))

    FakeLike = bt.Tuple[str, str, float]  # let the shennanigans commence

    @beartypeable(compiletime=TH(FakeLike))
    class Faker(bt.NamedTuple):
        name: str
        kind: str
        velocity: float

    FakeLike = bt.Tuple[str, str, float]  # let the shennanigans commence

    # this kinda __beartype__ expansion thing has to be automated...
    @beartypeable(compiletime=TH(bt.Tuple[int, Faker.__beartype__().hint]))
    class FakeEst(bt.NamedTuple):
        id: int
        fakestuff: Faker

    print(wrapped_is_bearable((1, ("hi", "bob", 2.8)), FakeEst))

    print(
        wrapped_is_bearable(
            FakeEst(1, Faker("hi", "bob", 2.8)), bt.Tuple[int, FakeLike]
        )
    )
