from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Numeric,
    Text,
    ForeignKey,
    Double,
)
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import TSVECTOR

from utils.utils import boolean_to_text
from models.BaseModel import AbstractMap


class PptAll(AbstractMap):
    __tablename__ = "ppt_all"
    gid = Column(Integer, primary_key=True, autoincrement=True)
    reg_num = Column(String(10))
    vid_ppt = Column(String(100))
    name = Column(String(254))
    vid_doc_ra = Column(String(100))
    num_doc_ra = Column(String(50))
    data_doc_r = Column(Date)
    zakazchik = Column(String(100))
    ispolnitel = Column(String(100))
    istoch_fin = Column(String(100))
    otvetst_mk = Column(String(50))
    num_kontra = Column(String(50))
    data_kontr = Column(Date)
    vid_doc_ut = Column(String(100))
    num_doc_ut = Column(String(50))
    data_doc_u = Column(Date)
    priostanov = Column(String(100))
    zaversheni = Column(String(100))
    otmena = Column(String(100))
    status = Column(String(40))
    grup1 = Column(String(100))
    grup2 = Column(String(100))
    oasi = Column(String(20))
    us_ppt = Column(String(10))
    sppgns_obs = Column(String(100))
    sppgns_jil = Column(String(100))
    sppgns_nej = Column(String(100))
    shape_area = Column(Numeric)
    geom = Column(Geometry("MULTIPOLYGON", 4326))

    @staticmethod
    def get_popup(row):
        return f"""
        <b>Регистрационный номер:</b> {row['reg_num']}<br>
        <b>Вид ППТ:</b> {row['vid_ppt']}<br>
        <b>Имя:</b> {row['name']}<br>
        <b>Вид документа РА:</b> {row['vid_doc_ra']}<br>
        <b>Номер документа РА:</b> {row['num_doc_ra']}<br>
        <b>Дата документа РА:</b> {row['data_doc_r']}<br>
        <b>Заказчик:</b> {row['zakazchik']}<br>
        <b>Исполнитель:</b> {row['ispolnitel']}<br>
        <b>Источник финансирования:</b> {row['istoch_fin']}<br>
        <b>Ответственный МК:</b> {row['otvetst_mk']}<br>
        <b>Номер контракта:</b> {row['num_kontra']}<br>
        <b>Дата контракта:</b> {row['data_kontr']}<br>
        <b>Вид документа УТ:</b> {row['vid_doc_ut']}<br>
        <b>Номер документа УТ:</b> {row['num_doc_ut']}<br>
        <b>Дата документа УТ:</b> {row['data_doc_u']}<br>
        <b>Приостановка:</b> {row['priostanov']}<br>
        <b>Завершение:</b> {row['zaversheni']}<br>
        <b>Отмена:</b> {row['otmena']}<br>
        <b>Статус:</b> {row['status']}<br>
        <b>Группа 1:</b> {row['grup1']}<br>
        <b>Группа 2:</b> {row['grup2']}<br>
        <b>OASI:</b> {row['oasi']}<br>
        <b>Условия ППТ:</b> {row['us_ppt']}<br>
        <b>Площадь:</b> {row['shape_area']} кв.м<br>
        """


class Rayon(AbstractMap):
    __tablename__ = "район"
    gid = Column(Integer, primary_key=True, autoincrement=True)
    objectid = Column(Double)
    uidnftn = Column(Double)
    name = Column(String(254))
    label = Column(String(254))
    address = Column(String(254))
    x = Column(Numeric)
    y = Column(Numeric)
    bui_no_bti = Column(Double)
    cad_no = Column(String(254))
    street_bti = Column(String(254))
    house_bti = Column(String(254))
    hadd_bti = Column(String(254))
    mun_obr = Column(String(200))
    moddate = Column(Date)
    moduser = Column(String(100))
    exclude_gr = Column(Numeric)
    shape_area = Column(Numeric)
    shape_len = Column(Numeric)
    geom = Column(Geometry("MULTIPOLYGON", 4326))

    @staticmethod
    def get_popup(row):
        return f"""
        <b>Название района:</b> {row['name']}<br>
        <b>Object ID:</b> {row['objectid']}<br>
        <b>UID NFTN:</b> {row['uidnftn']}<br>
        <b>Метка:</b> {row['label']}<br>
        <b>Адрес:</b> {row['address']}<br>
        <b>X:</b> {row['x']}<br>
        <b>Y:</b> {row['y']}<br>
        <b>BTI BUI No:</b> {row['bui_no_bti']}<br>
        <b>Кадастровый номер:</b> {row['cad_no']}<br>
        <b>BTI Улица:</b> {row['street_bti']}<br>
        <b>BTI Дом:</b> {row['house_bti']}<br>
        <b>BTI Адрес:</b> {row['hadd_bti']}<br>
        <b>Муниципальное образование:</b> {row['mun_obr']}<br>
        <b>Дата изменения:</b> {row['moddate']}<br>
        <b>Пользователь изменения:</b> {row['moduser']}<br>
        <b>Исключенная группа:</b> {row['exclude_gr']}<br>
        <b>Площадь:</b> {row['shape_area']} кв.м<br>
        <b>Длина:</b> {row['shape_len']}<br>
        """


class UDSMosty(AbstractMap):
    __tablename__ = "УДС_мосты"
    gid = Column(Integer, primary_key=True, autoincrement=True)
    name_obj = Column(String(6))
    state = Column(String(254))
    vid = Column(String(254))
    name = Column(String(80))
    shape_leng = Column(Numeric)
    shape_area = Column(Numeric)
    geom = Column(Geometry("MULTIPOLYGON", 4326))

    @staticmethod
    def get_popup(row):
        return f"""
        <b>Название моста:</b> {row['name_obj']}<br>
        <b>Состояние:</b> {row['state']}<br>
        <b>Вид:</b> {row['vid']}<br>
        <b>Имя:</b> {row['name']}<br>
        <b>Длина:</b> {row['shape_leng']}<br>
        <b>Площадь:</b> {row['shape_area']} кв.м<br>
        """


class KadastrDel(AbstractMap):
    __tablename__ = "Кадастровое деление"
    gid = Column(Integer, primary_key=True, autoincrement=True)
    cadastra1 = Column(String(80))
    objectid = Column(String(80))
    geom = Column(Geometry("MULTIPOLYGON", 4326))

    @staticmethod
    def get_popup(row):
        return f"""
        <b>Кадастровый номер:</b> {row['cadastra1']}<br>
        <b>Object ID:</b> {row['objectid']}<br>
        """


class Okrug(AbstractMap):
    __tablename__ = "округ"
    gid = Column(Integer, primary_key=True, autoincrement=True)
    objectid = Column(Double)
    uidnftn = Column(Double)
    name = Column(String(254))
    label = Column(String(254))
    address = Column(String(254))
    x = Column(Numeric)
    y = Column(Numeric)
    bui_no_bti = Column(Double)
    cad_no = Column(String(254))
    street_bti = Column(String(254))
    house_bti = Column(String(254))
    hadd_bti = Column(String(254))
    moddate = Column(Date)
    moduser = Column(String(100))
    torzid = Column(Numeric)
    exclude_gr = Column(Numeric)
    shape_area = Column(Numeric)
    shape_len = Column(Numeric)
    geom = Column(Geometry("MULTIPOLYGON", 4326))

    @staticmethod
    def get_popup(row):
        return f"""
        <b>Название округа:</b> {row['name']}<br>
        <b>Object ID:</b> {row['objectid']}<br>
        <b>UID NFTN:</b> {row['uidnftn']}<br>
        <b>Метка:</b> {row['label']}<br>
        <b>Адрес:</b> {row['address']}<br>
        <b>X:</b> {row['x']}<br>
        <b>Y:</b> {row['y']}<br>
        <b>BTI BUI No:</b> {row['bui_no_bti']}<br>
        <b>Кадастровый номер:</b> {row['cad_no']}<br>
        <b>BTI Улица:</b> {row['street_bti']}<br>
        <b>BTI Дом:</b> {row['house_bti']}<br>
        <b>BTI Адрес:</b> {row['hadd_bti']}<br>
        <b>Дата изменения:</b> {row['moddate']}<br>
        <b>Пользователь изменения:</b> {row['moduser']}<br>
        <b>Torz ID:</b> {row['torzid']}<br>
        <b>Исключенная группа:</b> {row['exclude_gr']}<br>
        <b>Площадь:</b> {row['shape_area']} кв.м<br>
        <b>Длина:</b> {row['shape_len']}<br>
        """


class PPGaz(AbstractMap):
    __tablename__ = "pp_gaz"
    gid = Column(Integer, primary_key=True, autoincrement=True)
    reg_num = Column(String(10))
    vid_ppt = Column(String(100))
    name = Column(String(254))
    vid_doc_ra = Column(String(100))
    num_doc_ra = Column(String(100))
    data_doc_r = Column(Date)
    zakazchik = Column(String(100))
    ispolnitel = Column(String(100))
    istoch_fin = Column(String(100))
    otvetst_mk = Column(String(50))
    num_kontra = Column(String(50))
    data_kontr = Column(Date)
    vid_doc_ut = Column(String(100))
    num_doc_ut = Column(String(50))
    data_doc_u = Column(Date)
    priostanov = Column(String(100))
    zaversheni = Column(String(100))
    otmena = Column(String(100))
    status = Column(String(50))
    grup1 = Column(String(100))
    grup2 = Column(String(100))
    oasi = Column(String(20))
    us_ppt = Column(String(10))
    shape_area = Column(Numeric)
    geom = Column(Geometry("MULTIPOLYGON", 4326))

    @staticmethod
    def get_popup(row):
        return f"""
        <b>Название газопровода:</b> {row['name']}<br>
        <b>Регистрационный номер:</b> {row['reg_num']}<br>
        <b>Вид ППТ:</b> {row['vid_ppt']}<br>
        <b>Имя:</b> {row['name']}<br>
        <b>Вид документа РА:</b> {row['vid_doc_ra']}<br>
        <b>Номер документа РА:</b> {row['num_doc_ra']}<br>
        <b>Дата документа РА:</b> {row['data_doc_r']}<br>
        <b>Заказчик:</b> {row['zakazchik']}<br>
        <b>Исполнитель:</b> {row['ispolnitel']}<br>
        <b>Источник финансирования:</b> {row['istoch_fin']}<br>
        <b>Ответственный МК:</b> {row['otvetst_mk']}<br>
        <b>Номер контракта:</b> {row['num_kontra']}<br>
        <b>Дата контракта:</b> {row['data_kontr']}<br>
        <b>Вид документа УТ:</b> {row['vid_doc_ut']}<br>
        <b>Номер документа УТ:</b> {row['num_doc_ut']}<br>
        <b>Дата документа УТ:</b> {row['data_doc_u']}<br>
        <b>Приостановка:</b> {row['priostanov']}<br>
        <b>Завершение:</b> {row['zaversheni']}<br>
        <b>Отмена:</b> {row['otmena']}<br>
        <b>Статус:</b> {row['status']}<br>
        <b>Группа 1:</b> {row['grup1']}<br>
        <b>Группа 2:</b> {row['grup2']}<br>
        <b>OASI:</b> {row['oasi']}<br>
        <b>Условия ППТ:</b> {row['us_ppt']}<br>
        <b>Площадь:</b> {row['shape_area']} кв.м<br>
        """


class KRT(AbstractMap):
    __tablename__ = "КРТ"
    gid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(254))
    area_krt = Column(Numeric)
    type_krt = Column(String(80))
    geom = Column(Geometry("MULTIPOLYGON", 4326))

    @staticmethod
    def get_popup(row):
        return f"""
        <b>Название КРТ:</b> {row['name']}<br>
        <b>Площадь:</b> {row['area_krt']} кв.м<br>
        <b>Тип КРТ:</b> {row['type_krt']}<br>
        """


class KvartalRegion(AbstractMap):
    __tablename__ = "kvartal_region"
    gid = Column(Integer, primary_key=True, autoincrement=True)
    objectid = Column(Double)
    num_doc_ut = Column(String(20))
    data_doc_u = Column(Date)
    name_ppt = Column(String(254))
    okrug = Column(String(10))
    rayon = Column(String(254))
    area = Column(Numeric)
    prim = Column(String(254))
    uslov = Column(Integer)
    db2gse_st_ = Column(Numeric)
    db2gse_sde = Column(Numeric)
    geom = Column(Geometry("MULTIPOLYGONZM", 4326))

    @staticmethod
    def get_popup(row):
        return f"""
        <b>Название квартала:</b> {row['name_ppt']}<br>
        <b>Object ID:</b> {row['objectid']}<br>
        <b>Номер документа УТ:</b> {row['num_doc_ut']}<br>
        <b>Дата документа УТ:</b> {row['data_doc_u']}<br>
        <b>Название ППТ:</b> {row['name_ppt']}<br>
        <b>Округ:</b> {row['okrug']}<br>
        <b>Район:</b> {row['rayon']}<br>
        <b>Площадь:</b> {row['area']} кв.м<br>
        <b>Примечание:</b> {row['prim']}<br>
        <b>Условие:</b> {row['uslov']}<br>
        <b>DB2GSE ST:</b> {row['db2gse_st_']}<br>
        <b>DB2GSE SDE:</b> {row['db2gse_sde']}<br>
        """


class PPMetroAll(AbstractMap):
    __tablename__ = "pp_metro_all"
    gid = Column(Integer, primary_key=True, autoincrement=True)
    reg_num = Column(String(10))
    vid_ppt = Column(String(100))
    name = Column(String(254))
    vid_doc_ra = Column(String(100))
    num_doc_ra = Column(String(100))
    data_doc_r = Column(Date)
    zakazchik = Column(String(100))
    ispolnitel = Column(String(100))
    istoch_fin = Column(String(100))
    otvetst_mk = Column(String(50))
    num_kontra = Column(String(50))
    data_kontr = Column(Date)
    vid_doc_ut = Column(String(100))
    num_doc_ut = Column(String(50))
    data_doc_u = Column(Date)
    priostanov = Column(String(100))
    zaversheni = Column(String(100))
    otmena = Column(String(100))
    status = Column(String(50))
    grup1 = Column(String(100))
    grup2 = Column(String(100))
    oasi = Column(String(20))
    us_ppt = Column(String(10))
    shape_area = Column(Numeric)
    geom = Column(Geometry("MULTIPOLYGON", 4326))

    @staticmethod
    def get_popup(row):
        return f"""
        <b>Название метро:</b> {row['name']}<br>
        <b>Регистрационный номер:</b> {row['reg_num']}<br>
        <b>Вид ППТ:</b> {row['vid_ppt']}<br>
        <b>Имя:</b> {row['name']}<br>
        <b>Вид документа РА:</b> {row['vid_doc_ra']}<br>
        <b>Номер документа РА:</b> {row['num_doc_ra']}<br>
        <b>Дата документа РА:</b> {row['data_doc_r']}<br>
        <b>Заказчик:</b> {row['zakazchik']}<br>
        <b>Исполнитель:</b> {row['ispolnitel']}<br>
        <b>Источник финансирования:</b> {row['istoch_fin']}<br>
        <b>Ответственный МК:</b> {row['otvetst_mk']}<br>
        <b>Номер контракта:</b> {row['num_kontra']}<br>
        <b>Дата контракта:</b> {row['data_kontr']}<br>
        <b>Вид документа УТ:</b> {row['vid_doc_ut']}<br>
        <b>Номер документа УТ:</b> {row['num_doc_ut']}<br>
        <b>Дата документа УТ:</b> {row['data_doc_u']}<br>
        <b>Приостановка:</b> {row['priostanov']}<br>
        <b>Завершение:</b> {row['zaversheni']}<br>
        <b>Отмена:</b> {row['otmena']}<br>
        <b>Статус:</b> {row['status']}<br>
        <b>Группа 1:</b> {row['grup1']}<br>
        <b>Группа 2:</b> {row['grup2']}<br>
        <b>OASI:</b> {row['oasi']}<br>
        <b>Условия ППТ:</b> {row['us_ppt']}<br>
        <b>Площадь:</b> {row['shape_area']} кв.м<br>
        """


class OKS(AbstractMap):
    __tablename__ = "ОКС"
    gid = Column(Integer, primary_key=True, autoincrement=True)
    unom = Column(Numeric)
    address = Column(String(254))
    cadastra3 = Column(String(80))
    hascadas4 = Column(String(80))
    hasbti = Column(String(80))
    hascontr6 = Column(Numeric)
    hasownrf = Column(String(80))
    hasownmo8 = Column(String(80))
    hasownot9 = Column(String(80))
    shape_area = Column(Numeric)
    geom = Column(Geometry("MULTIPOLYGON", 4326))

    @staticmethod
    def get_popup(row):
        return f"""
        <b>Адрес:</b> {row['address']}<br>
        <b>UNOM:</b> {row['unom']}<br>
        <b>Кадастровый номер 3:</b> {row['cadastra3']}<br>
        <b>Кадастровый номер 4:</b> {row['hascadas4']}<br>
        <b>BTI:</b> {row['hasbti']}<br>
        <b>Контракт 6:</b> {row['hascontr6']}<br>
        <b>Владение РФ:</b> {row['hasownrf']}<br>
        <b>Владение МО:</b> {row['hasownmo8']}<br>
        <b>Владение другое:</b> {row['hasownot9']}<br>
        <b>Площадь:</b> {row['shape_area']} кв.м<br>
        """


class OOZT(AbstractMap):
    __tablename__ = "ООЗТ"
    gid = Column(Integer, primary_key=True, autoincrement=True)
    objectid = Column(String(80))
    status = Column(String(80))
    zoneid = Column(String(80))
    docnum = Column(String(80))
    docdate = Column(String(80))
    doclist = Column(String(254))
    geom = Column(Geometry("MULTIPOLYGON", 4326))

    @staticmethod
    def get_popup(row):
        return f"""
        <b>ID объекта:</b> {row['objectid']}<br>
        <b>Статус:</b> {row['status']}<br>
        <b>Zone ID:</b> {row['zoneid']}<br>
        <b>Номер документа:</b> {row['docnum']}<br>
        <b>Дата документа:</b> {row['docdate']}<br>
        <b>Список документов:</b> {row['doclist']}<br>
        """


class UDSDorogi(AbstractMap):
    __tablename__ = "УДС_дороги"
    gid = Column(Integer, primary_key=True, autoincrement=True)
    name_obj = Column(String(4))
    name_str = Column(String(254))
    vid_road = Column(String(254))
    ext_name = Column(String(254))
    shape_leng = Column(Numeric)
    shape_area = Column(Numeric)
    geom = Column(Geometry("MULTIPOLYGON", 4326))

    @staticmethod
    def get_popup(row):
        return f"""
        <b>Название дороги:</b> {row['name_obj']}<br>
        <b>Название улицы:</b> {row['name_str']}<br>
        <b>Вид дороги:</b> {row['vid_road']}<br>
        <b>Дополнительное название:</b> {row['ext_name']}<br>
        <b>Длина:</b> {row['shape_leng']}<br>
        <b>Площадь:</b> {row['shape_area']} кв.м<br>
        """


class TpuRvMetroPolygon(AbstractMap):
    __tablename__ = "tpu_rv_metro_polygon"
    gid = Column(Integer, primary_key=True, autoincrement=True)
    reg_num = Column(String(10))
    vid_ppt = Column(String(100))
    name = Column(String(254))
    vid_doc_ra = Column(String(100))
    num_doc_ra = Column(String(100))
    data_doc_r = Column(Date)
    zakazchik = Column(String(100))
    ispolnitel = Column(String(100))
    istoch_fin = Column(String(100))
    otvetst_mk = Column(String(50))
    num_kontra = Column(String(50))
    data_kontr = Column(Date)
    vid_doc_ut = Column(String(100))
    num_doc_ut = Column(String(50))
    data_doc_u = Column(Date)
    priostanov = Column(String(100))
    zaversheni = Column(String(100))
    otmena = Column(String(100))
    status = Column(String(50))
    grup1 = Column(String(100))
    grup2 = Column(String(100))
    oasi = Column(String(20))
    us_ppt = Column(String(10))
    sppgns_obs = Column(String(100))
    sppgns_jil = Column(String(100))
    sppgns_nej = Column(String(100))
    shape_area = Column(Numeric)
    geom = Column(Geometry("MULTIPOLYGON", 4326))

    @staticmethod
    def get_popup(row):
        return f"""
        <b>Название ТПУ:</b> {row['name']}<br>
        <b>Регистрационный номер:</b> {row['reg_num']}<br>
        <b>Вид ППТ:</b> {row['vid_ppt']}<br>
        <b>Имя:</b> {row['name']}<br>
        <b>Вид документа РА:</b> {row['vid_doc_ra']}<br>
        <b>Номер документа РА:</b> {row['num_doc_ra']}<br>
        <b>Дата документа РА:</b> {row['data_doc_r']}<br>
        <b>Заказчик:</b> {row['zakazchik']}<br>
        <b>Исполнитель:</b> {row['ispolnitel']}<br>
        <b>Источник финансирования:</b> {row['istoch_fin']}<br>
        <b>Ответственный МК:</b> {row['otvetst_mk']}<br>
        <b>Номер контракта:</b> {row['num_kontra']}<br>
        <b>Дата контракта:</b> {row['data_kontr']}<br>
        <b>Вид документа УТ:</b> {row['vid_doc_ut']}<br>
        <b>Номер документа УТ:</b> {row['num_doc_ut']}<br>
        <b>Дата документа УТ:</b> {row['data_doc_u']}<br>
        <b>Приостановка:</b> {row['priostanov']}<br>
        <b>Завершение:</b> {row['zaversheni']}<br>
        <b>Отмена:</b> {row['otmena']}<br>
        <b>Статус:</b> {row['status']}<br>
        <b>Группа 1:</b> {row['grup1']}<br>
        <b>Группа 2:</b> {row['grup2']}<br>
        <b>OASI:</b> {row['oasi']}<br>
        <b>Условия ППТ:</b> {row['us_ppt']}<br>
        <b>SPPGNS OBS:</b> {row['sppgns_obs']}<br>
        <b>SPPGNS JIL:</b> {row['sppgns_jil']}<br>
        <b>SPPGNS NEJ:</b> {row['sppgns_nej']}<br>
        <b>Площадь:</b> {row['shape_area']} кв.м<br>
        """


class Spritzones(AbstractMap):
    __tablename__ = "spritzones_2024_04_18_12_16_48"
    gid = Column(Integer, primary_key=True, autoincrement=True)
    linecode = Column(String(254))
    name = Column(String(254))
    doc = Column(String(254))
    comment = Column(String(254))
    area = Column(Numeric)
    geom = Column(Geometry("MULTIPOLYGON", 4326))

    @staticmethod
    def get_popup(row):
        return f"""
        <b>Название зоны:</b> {row['name']}<br>
        <b>Код линии:</b> {row['linecode']}<br>
        <b>Документ:</b> {row['doc']}<br>
        <b>Комментарий:</b> {row['comment']}<br>
        <b>Площадь:</b> {row['area']} кв.м<br>
        """


class StartovPloshchRenov(AbstractMap):
    __tablename__ = "Стартовые площадки реновации"
    gid = Column(Integer, primary_key=True, autoincrement=True)
    okrug = Column(String(80))
    rayon = Column(String(80))
    address = Column(String(254))
    area = Column(String(80))
    prim = Column(String(115))
    plotnost = Column(String(80))
    vysota = Column(String(80))
    spp = Column(String(80))
    total_area = Column(String(80))
    flat_area = Column(String(80))
    osnovanie = Column(String(254))
    agr = Column(String(254))
    objectid = Column(String(80))
    geom = Column(Geometry("MULTIPOLYGON", 4326))

    @staticmethod
    def get_popup(row):
        return f"""
        <b>Адрес:</b> {row['address']}<br>
        <b>Округ:</b> {row['okrug']}<br>
        <b>Район:</b> {row['rayon']}<br>
        <b>Адрес:</b> {row['address']}<br>
        <b>Площадь:</b> {row['area']} кв.м<br>
        <b>Примечание:</b> {row['prim']}<br>
        <b>Плотность:</b> {row['plotnost']}<br>
        <b>Высота:</b> {row['vysota']}<br>
        <b>SPP:</b> {row['spp']}<br>
        <b>Общая площадь:</b> {row['total_area']}<br>
        <b>Площадь квартиры:</b> {row['flat_area']}<br>
        <b>Основание:</b> {row['osnovanie']}<br>
        <b>AGR:</b> {row['agr']}<br>
        <b>Object ID:</b> {row['objectid']}<br>
        """


class TpzNew(AbstractMap):
    __tablename__ = "tpz_new"
    gid = Column(Integer, primary_key=True, autoincrement=True)
    podzone_nu = Column(String(25))
    num_pp = Column(String(50))
    doc_date = Column(Date)
    type = Column(String(50))
    plotnost = Column(String(50))
    vysota = Column(String(50))
    proczastro = Column(String(50))
    area = Column(Numeric)
    geom = Column(Geometry("MULTIPOLYGON", 4326))

    @staticmethod
    def get_popup(row):
        return f"""
        <b>Номер подзоны:</b> {row['podzone_nu']}<br>
        <b>Номер ПП:</b> {row['num_pp']}<br>
        <b>Дата документа:</b> {row['doc_date']}<br>
        <b>Тип:</b> {row['type']}<br>
        <b>Плотность:</b> {row['plotnost']}<br>
        <b>Высота:</b> {row['vysota']}<br>
        <b>Процент застройки:</b> {row['proczastro']}<br>
        <b>Площадь:</b> {row['area']} кв.м<br>
        """


class TzNew(AbstractMap):
    __tablename__ = "tz_new"
    gid = Column(Integer, primary_key=True, autoincrement=True)
    zone_num = Column(String(20))
    num_pp = Column(String(50))
    doc_date = Column(Date)
    type = Column(String(50))
    index_ = Column(String(254))
    vri_540 = Column(String(254))
    area = Column(Numeric)
    geom = Column(Geometry("MULTIPOLYGON", 4326))

    @staticmethod
    def get_popup(row):
        return f"""
        <b>Номер зоны:</b> {row['zone_num']}<br>
        <b>Номер ПП:</b> {row['num_pp']}<br>
        <b>Дата документа:</b> {row['doc_date']}<br>
        <b>Тип:</b> {row['type']}<br>
        <b>Индекс:</b> {row['index_']}<br>
        <b>ВРИ:</b> {row['vri_540']}<br>
        <b>Площадь:</b> {row['area']} кв.м<br>
        """


class PptUDS(AbstractMap):
    __tablename__ = "ppt_uds"
    gid = Column(Integer, primary_key=True, autoincrement=True)
    reg_num = Column(String(10))
    vid_ppt = Column(String(100))
    name = Column(String(254))
    vid_doc_ra = Column(String(100))
    num_doc_ra = Column(String(100))
    data_doc_r = Column(Date)
    zakazchik = Column(String(100))
    ispolnitel = Column(String(100))
    istoch_fin = Column(String(100))
    otvetst_mk = Column(String(50))
    num_kontra = Column(String(50))
    data_kontr = Column(Date)
    vid_doc_ut = Column(String(100))
    num_doc_ut = Column(String(50))
    data_doc_u = Column(Date)
    priostanov = Column(String(100))
    zaversheni = Column(String(100))
    otmena = Column(String(100))
    status = Column(String(50))
    grup1 = Column(String(100))
    grup2 = Column(String(100))
    oasi = Column(String(20))
    us_ppt = Column(String(10))
    shape_area = Column(Numeric)
    geom = Column(Geometry("MULTIPOLYGON", 4326))

    @staticmethod
    def get_popup(row):
        return f"""
        <b>Название УДС:</b> {row['name']}<br>
        <b>Регистрационный номер:</b> {row['reg_num']}<br>
        <b>Вид ППТ:</b> {row['vid_ppt']}<br>
        <b>Имя:</b> {row['name']}<br>
        <b>Вид документа РА:</b> {row['vid_doc_ra']}<br>
        <b>Номер документа РА:</b> {row['num_doc_ra']}<br>
        <b>Дата документа РА:</b> {row['data_doc_r']}<br>
        <b>Заказчик:</b> {row['zakazchik']}<br>
        <b>Исполнитель:</b> {row['ispolnitel']}<br>
        <b>Источник финансирования:</b> {row['istoch_fin']}<br>
        <b>Ответственный МК:</b> {row['otvetst_mk']}<br>
        <b>Номер контракта:</b> {row['num_kontra']}<br>
        <b>Дата контракта:</b> {row['data_kontr']}<br>
        <b>Вид документа УТ:</b> {row['vid_doc_ut']}<br>
        <b>Номер документа УТ:</b> {row['num_doc_ut']}<br>
        <b>Дата документа УТ:</b> {row['data_doc_u']}<br>
        <b>Приостановка:</b> {row['priostanov']}<br>
        <b>Завершение:</b> {row['zaversheni']}<br>
        <b>Отмена:</b> {row['otmena']}<br>
        <b>Статус:</b> {row['status']}<br>
        <b>Группа 1:</b> {row['grup1']}<br>
        <b>Группа 2:</b> {row['grup2']}<br>
        <b>OASI:</b> {row['oasi']}<br>
        <b>Условия ППТ:</b> {row['us_ppt']}<br>
        <b>Площадь:</b> {row['shape_area']} кв.м<br>
        """


class UchastkiMezhev(AbstractMap):
    __tablename__ = "участки_межевания"
    gid = Column(Integer, primary_key=True, autoincrement=True)
    numberarea = Column(Integer)
    descr = Column(String(254))
    klass = Column(String(254))
    func_use = Column(String(254))
    n_kvar = Column(String(50))
    n_parc = Column(String(50))
    year = Column(String(50))
    area = Column(Numeric)
    shape_area = Column(Numeric)
    geom = Column(Geometry("MULTIPOLYGON", 4326))

    @staticmethod
    def get_popup(row):
        return f"""
        <b>Описание:</b> {row['descr']}<br>
        <b>Номер участка:</b> {row['numberarea']}<br>
        <b>Класс:</b> {row['klass']}<br>
        <b>Функциональное использование:</b> {row['func_use']}<br>
        <b>Номер квартиры:</b> {row['n_kvar']}<br>
        <b>Номер участка:</b> {row['n_parc']}<br>
        <b>Год:</b> {row['year']}<br>
        <b>Площадь:</b> {row['area']} кв.м<br>
        <b>Площадь фигуры:</b> {row['shape_area']}<br>
        """


class Zouit(AbstractMap):
    __tablename__ = "zouit"
    gid = Column(Integer, primary_key=True, autoincrement=True)
    cad_num = Column(String(254))
    okrug = Column(String(254))
    raion_pos = Column(String(254))
    vid_zouit = Column(String(254))
    type_zone = Column(String(254))
    name = Column(String(254))
    ogran = Column(String(254))
    doc = Column(String(254))
    area = Column(Numeric)
    geom = Column(Geometry("MULTIPOLYGON", 4326))

    @staticmethod
    def get_popup(row):
        return f"""
        <b>Название зоны:</b> {row['name']}<br>
        <b>Кадастровый номер:</b> {row['cad_num']}<br>
        <b>Округ:</b> {row['okrug']}<br>
        <b>Район:</b> {row['raion_pos']}<br>
        <b>Вид ЗОУИТ:</b> {row['vid_zouit']}<br>
        <b>Тип зоны:</b> {row['type_zone']}<br>
        <b>Имя:</b> {row['name']}<br>
        <b>Ограничение:</b> {row['ogran']}<br>
        <b>Документ:</b> {row['doc']}<br>
        <b>Площадь:</b> {row['area']} кв.м<br>
        """


class ZU(AbstractMap):
    __tablename__ = "ЗУ"
    gid = Column(Integer, primary_key=True, autoincrement=True)
    cadastra2 = Column(String(80))
    address = Column(String(254))
    hasvalid5 = Column(String(80))
    hascadas6 = Column(String(80))
    isdraft = Column(String(80))
    ownershi8 = Column(Numeric)
    is_stroy = Column(String(80))
    is_nonca20 = Column(Numeric)
    area = Column(Numeric)
    geom = Column(Geometry("MULTIPOLYGON", 4326))
    district_id = Column(Integer, ForeignKey("округ.gid"))
    comments = Column(Text)
    address_tsv = Column(TSVECTOR)

    @staticmethod
    def get_popup(row):
        return f"""
        <b>Кадастровый номер:</b> {row['cadastra2']}<br>
        <b>Адрес:</b> {row['address']}<br>
        <b>Действующий документ:</b> {boolean_to_text(row['hasvalid5'])}<br>
        <b>Кадастровый учет:</b> {boolean_to_text(row['hascadas6'])}<br>
        <b>Проект:</b> {boolean_to_text(row['isdraft'])}<br>
        <b>Собственность:</b> {row['ownershi8']}<br>
        <b>Разрешение на строительство:</b> {boolean_to_text(row['is_stroy'])}<br>
        <b>Некапитальные объекты:</b> {boolean_to_text(row['is_nonca20'])}<br>
        <b>Площадь:</b> {row['area']} кв.м<br>
        <b>Комментарии:</b> {row['comments']}<br>
        <form onsubmit="saveComment(event, {row['gid']})">
            <textarea name="comment" rows="2" cols="30" placeholder="Добавить комментарий"></textarea><br>
            <input type="submit" value="Сохранить">
        </form>
        """


class MKD(AbstractMap):
    __tablename__ = "МКД"

    gid = Column(Integer, primary_key=True, autoincrement=True)
    unom = Column(Numeric)
    address = Column(String(254))
    cadastra3 = Column(String(80))
    hascadas4 = Column(String(80))
    hasbti = Column(String(80))
    hascontr6 = Column(Numeric)
    hasownrf = Column(String(80))
    hasownmo8 = Column(String(80))
    hasownot9 = Column(String(80))
    cadastra10 = Column(String(80))
    mgsntype = Column(String(80))
    hasmgsn = Column(String(80))
    cadastra13 = Column(String(80))
    btitype = Column(String(80))
    objectid = Column(String(80))
    mkd_flag = Column(Numeric)
    moddate = Column(String(80))
    geom = Column(Geometry("MULTIPOLYGON", 4326))

    @staticmethod
    def get_popup(row):
        return f"""
        <b>УНОМ:</b> {row['unom']}<br>
        <b>Адрес:</b> {row['address']}<br>
        <b>Кадастр 3:</b> {row['cadastra3']}<br>
        <b>Есть кадастр 4:</b> {row['hascadas4']}<br>
        <b>Есть БТИ:</b> {row['hasbti']}<br>
        <b>Есть контракт 6:</b> {row['hascontr6']}<br>
        <b>Есть собственность РФ:</b> {row['hasownrf']}<br>
        <b>Есть собственность МО 8:</b> {row['hasownmo8']}<br>
        <b>Есть другая собственность 9:</b> {row['hasownot9']}<br>
        <b>Кадастр 10:</b> {row['cadastra10']}<br>
        <b>Тип МГСН:</b> {row['mgsntype']}<br>
        <b>Есть МГСН:</b> {row['hasmgsn']}<br>
        <b>Кадастр 13:</b> {row['cadastra13']}<br>
        <b>Тип БТИ:</b> {row['btitype']}<br>
        <b>Идентификатор объекта:</b> {row['objectid']}<br>
        <b>Флаг МКД:</b> {row['mkd_flag']}<br>
        <b>Дата изменения:</b> {row['moddate']}<br>
        """
