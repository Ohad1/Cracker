import string
from random import choice, sample

import pytest
import hashlib
from Master.HashValidator import HashValidator


def generate_random_string(n=20):
    return ''.join(choice(string.ascii_letters + string.digits) for _ in range(n))


VALID_HASHES_LIST = [hashlib.md5(generate_random_string(i).encode()).hexdigest() for i in range(50)]
VALID_HASHES_LISTS = [sample(VALID_HASHES_LIST, i) for i in range(len(VALID_HASHES_LIST))]
VALID_HASHES_LISTS = [hash_list for hash_list in VALID_HASHES_LISTS if hash_list]

INVALID_HASHES_LIST = ['dq*-UmG_f^_8$\\*K9FaL5suo\x0c-Qr)}|q', 'XUb\n7kx^4DYK4#3M.Z|]}})zJ @Q-5p ',
                       "qD[(&.^2%MXB*D'?7H\ngsQJ@5zSG!xt?", '%-/T&eTzl/v?z._`Ie[]37`@iaA stHM',
                       '&9sD\t9M#]Ih@""FCnXEx\n"Db91qRQm[y', '\t0kDt92%Ul1jZL_ ayc\n\nkZ2WX>\nTaK<',
                       'aP5>]P[@],#\x0b}Dk9~nJm6q\x0b(\\\tVe\r;.1', 'A>fMpDjM\rUj3id!NA$l!Xu>3#+cM`^~O',
                       'C/65&W1~6i8*eNp\'3L9[$9f"V,M!irxl', '9xGw7(sOW_^SFf\r6dN[?>kL]2wJOj_up',
                       ")+'8&<6=gc{|6zm(ebmx+l\\J(r,n>,u9", '*#W8 ~H#8|M8(q6\x0bbb>y"VzZ8g_]Ze`#',
                       'r*LQm` Q"paY93LG$;#8?_8MiRX<Q9\x0bY', 'HbMDu3/C(1,\r<&!eBA>]$~^O\x0bS5@bYo{',
                       '>051(.b{ `QvuV|+qg&*A@|4dm+>Xf,j', '7ta6.k64kt?VgiPTYug}GO(UQ{mwQw@\n',
                       "M+@)qZ8' FIM@5&_CHi1<\t6:2PnGj?c*", 'fl#&i\\Uo}Vps4R\x0b\x0b7nwI\x0c7Ch*\\3rFf O',
                       "(@|'+(wEzCz 'PxSebESTu@K@fFjg-\r$", 'N+\nSROo;zp?>47p\r#\\&%$G=D,v`E1oT"',
                       'Z!%X~GiHplli2nk4T\tua!jx:ute*fZBR', 'x8VOCPj,sP]+cES\nm9\t;kkDFZ1X$~,.K',
                       'W#Fok\tCI49LBzR*\x0ci\\D&&peqmG\x0by;7J%', 'LM#O34Xs&>Y;.0LH&(bioBTYH$%BGj\n~',
                       ')w\x0c(\\D<=]>\\1y\x0b/#\\%ZzKG9KY|8LoC\r&', '\rdQG(Q9Y\x0bFDI0w\n>"xr2SrEg`um-*nv}',
                       '"\r<yICX0d+mP:)G;cC]\x0bLYtXtTf(J)@0', '?zDF]%s\\Q+yPE/q*B9FJeDMh9Q)zKnM|',
                       'NPL1|N;OAqBt.\\ q9YYBTr]J)_<=im\\G'
                       'dfg#%$$HFDGH&I^&I', 'FGHDFHGDFGHDHgh*q243c2v54yr', '!@#$%^&*()!@#$%^&*()!@#$%^&*()gt',
                       'py5f\t\x0cuI`jvSw\x0b<sg\'Iqx?{_E\rL"*kTp',
                       '']
INVALID_HASHES_LISTS = [sample(INVALID_HASHES_LIST, i) for i in range(len(INVALID_HASHES_LIST))]
INVALID_HASHES_LISTS = [hash_list for hash_list in INVALID_HASHES_LISTS if hash_list]


@pytest.fixture(params=VALID_HASHES_LISTS)
def valid_hashes(request):
    return request.param


def test_valid_hashes(valid_hashes):
    hash_validator = HashValidator(valid_hashes)
    assert hash_validator.validate_hashes()


@pytest.fixture(params=INVALID_HASHES_LISTS)
def invalid_hashes(request):
    return request.param


def test_invalid_hashes(invalid_hashes):
    hash_validator = HashValidator(invalid_hashes)
    assert not hash_validator.validate_hashes()
