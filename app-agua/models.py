from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, BIGINT, Double, DateTime
from sqlalchemy.orm import relationship

from database import Base

from typing import List, Optional
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
  pass

class Tipo_Usuario(Base):
    __tablename__ = "tipo_usuarios"

    id_tipo: Mapped[Optional[int]] = mapped_column(BIGINT, primary_key=True)
    desc_tipo: Mapped[str] = mapped_column(String(20))

    usuario: Mapped["Usuario"] = relationship(back_populates="tipo")

    def __repr__(self) -> str:
        return f"Tipo_Usuario(id={self.id_tipo!r}, desc_tipo={self.desc_tipo!r})"


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario: Mapped[Optional[int]] = mapped_column(BIGINT, primary_key=True)
    usuario: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(150))
    id_tipo: Mapped[int] = mapped_column(BIGINT, ForeignKey("tipo_usuarios.id_tipo"))

    tipo: Mapped["Tipo_Usuario"] = relationship(back_populates="usuario")
    grupos: Mapped[List["Grupo"]] = relationship(back_populates="usuario", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Usuario(id={self.id_usuario!r}, usuario={self.usuario!r})"


class Grupo(Base):
    __tablename__="grupos"

    id_grupo: Mapped[Optional[int]] = mapped_column(BIGINT, primary_key=True)
    id_usuario: Mapped[int] = mapped_column(BIGINT, ForeignKey("usuarios.id_usuario"))
    nombre: Mapped[str] = mapped_column(String(50))

    usuario: Mapped["Usuario"] = relationship(back_populates="grupos")
    vinculacion: Mapped["Vinculacion_Grupo"] = relationship(back_populates="grupo",cascade="all, delete-orphan")
    almacenamientos: Mapped[List["Almacenamiento"]] = relationship(back_populates="grupo", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Grupo(id={self.id_grupo!r}, nombre={self.nombre!r})"


class Vinculacion_Grupo(Base):
    __tablename__="vinculacion_grupos"

    id_vinculacion: Mapped[Optional[int]] = mapped_column(BIGINT, primary_key=True)
    id_grupo: Mapped[int] = mapped_column(BIGINT, ForeignKey("grupos.id_grupo"))
    usuario_vinculacion: Mapped[str] = mapped_column(String(50))
    clave_vinculacion: Mapped[str] = mapped_column(String(150))

    grupo: Mapped["Grupo"] = relationship(back_populates="vinculacion")

    def __repr__(self) -> str:
        return f"Vinculacion_Grupo(id={self.id_vinculacion!r}, usuario_grupo={self.usuario_vinculacion!r})"


class Almacenamiento(Base):
    __tablename__="almacenamientos"

    id_almacenamiento: Mapped[Optional[int]] = mapped_column(BIGINT, primary_key=True)
    id_grupo: Mapped[int] = mapped_column(BIGINT, ForeignKey("grupos.id_grupo"))
    capacidad_maxima: Mapped[float] = mapped_column(Double)
    ubicacion: Mapped[str] = mapped_column(String(20))

    grupo: Mapped["Grupo"] = relationship(back_populates="almacenamientos")
    dispo_IoT: Mapped["IoT"] = relationship(back_populates="almacenamiento", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Almacenamiento(id={self.id_almacenamiento!r}, capacidad_maxima={self.capacidad_maxima!r}, ubicacion={self.ubicacion!r})"


class IoT(Base):
    __tablename__="vinculacion_IoT"

    id_vin_IoT: Mapped[Optional[int]] = mapped_column(BIGINT, primary_key=True)
    id_almacenamiento: Mapped[int] = mapped_column(BIGINT, ForeignKey("almacenamientos.id_almacenamiento"))
    dispo_IoT: Mapped[str] = mapped_column(String(50))

    almacenamiento: Mapped["Almacenamiento"] = relationship(back_populates="dispo_IoT")
    variables: Mapped[List["Recepcion_Datos"]] = relationship(back_populates="dispositivo", cascade="all, delete-orphan")
    entradas: Mapped[List["Entrada_Agua"]] = relationship(back_populates="dispositivo", cascade="all, delete-orphan")
    salidas: Mapped[List["Salida_Agua"]] = relationship(back_populates="dispositivo", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"IoT(id={self.id_vin_IoT!r}, dispositivo_IoT={self.dispo_IoT!r})"


class Recepcion_Datos(Base):
    __tablename__="recepcion_variables"

    id_recepcion: Mapped[Optional[int]] = mapped_column(BIGINT, primary_key=True)
    id_vin_IoT: Mapped[int] = mapped_column(BIGINT, ForeignKey("vinculacion_IoT.id_vin_IoT"))
    nivel_actual: Mapped[float] = mapped_column(Double)
    Boya1: Mapped[bool] = mapped_column(Boolean)
    Boya2: Mapped[bool] = mapped_column(Boolean)
    Boya3: Mapped[bool] = mapped_column(Boolean)
    BoyaP: Mapped[bool] = mapped_column(Boolean)
    Estado_Bomba: Mapped[bool] = mapped_column(Boolean)
    Fecha_Hora: Mapped[str] = mapped_column(DateTime)

    dispositivo: Mapped["IoT"] = relationship(back_populates="variables")

    def __repr__(self) -> str:
        return f"Recepcion(id={self.id_recepcion!r}, nivel_actual={self.nivel_actual!r}, Boya 1={self.Boya1!r},Boya 2={self.Boya2!r}, Boya 3={self.Boya3!r}, Boya Principal={self.BoyaP}, Estado Bomba={self.Estado_Bomba!r}, Fecha_Hora={self.Fecha_Hora!r})"


class Entrada_Agua(Base):
    __tablename__="llenado_agua"

    id_llenado: Mapped[Optional[int]] = mapped_column(BIGINT, primary_key=True)
    id_vin_IoT: Mapped[int] = mapped_column(BIGINT, ForeignKey("vinculacion_IoT.id_vin_IoT"))
    cantidad_entrada: Mapped[float] = mapped_column(Double)
    Fecha_Hora: Mapped[str] = mapped_column(DateTime)

    dispositivo: Mapped["IoT"] = relationship(back_populates="entradas")

    def __repr__(self) -> str:
        return f"Entrada_Agua(id={self.id_llenado!r}, Cantidad={self.cantidad_entrada!r}, Fecha_Hora={self.Fecha_Hora!r})"


class Salida_Agua(Base):
    __tablename__="consumo_agua"

    id_consumo: Mapped[Optional[int]] = mapped_column(BIGINT, primary_key=True)
    id_vin_IoT: Mapped[int] = mapped_column(BIGINT, ForeignKey("vinculacion_IoT.id_vin_IoT"))
    cantidad_salida: Mapped[float] = mapped_column(Double)
    Fecha_Hora: Mapped[str] = mapped_column(DateTime)

    dispositivo: Mapped["IoT"] = relationship(back_populates="salidas")

    def __repr__(self) -> str:
        return f"Salida_Agua(id={self.id_consumo!r}, Cantidad={self.cantidad_salida!r}, Fecha_Hora={self.Fecha_Hora!r})"

