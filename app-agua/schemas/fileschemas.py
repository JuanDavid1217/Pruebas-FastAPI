from pydantic import BaseModel

#--------Tipos de Usuarios--------#

class Tipo_UsuarioBase(BaseModel):
    desc_tipo: str | None = None


class Tipo_UsuarioCreate(Tipo_UsuarioBase):
    pass


class Tipo_Usuario(Tipo_UsuarioBase):
    id_tipo: int | None = None


    class Config:
        orm_mode = True


#---------Vinculaciones (Usuario y Contraseña por grupo)-------#

class VinculacionBase(BaseModel):
    usuario_vinculacion: str | None = None


class VinculacionCreate(VinculacionBase):
    id_grupo: int
    clave_vinculacion: str | None = None


class Vinculacion_Grupo(VinculacionBase):
    id_vinculacion: int | None = None

    class Config:
        orm_mode = True


#--------Recepcion de variables generales-------#

class Recepcion_DatosBase(BaseModel):
    nivel_actual: float | None = None
    Boya1: bool | None = None
    Boya2: bool | None = None
    Boya3: bool | None = None
    BoyaP: bool | None = None
    Estado_Bomba: bool | None = None
    Fecha_Hora: str | None = None

class Recepcion_DatosVin(Recepcion_DatosBase):
    dispo_IoT: str | None = None

class Recepcion_DatosCreate(Recepcion_DatosBase):
    id_vin_IoT: int | None = None

class Recepcion_Datos(Recepcion_DatosBase):
    id_recepcion: int | None = None

    class Config:
        orm_mode = True


#-------Llenado de agua (Entrada)------#

class Entrada_AguaBase(BaseModel):
    cantidad_entrada: float | None = None
    Fecha_Hora: str | None = None

class Entrada_AguaVin(Entrada_AguaBase):
    dispo_IoT: str | None = None

class Entrada_AguaCreate(Entrada_AguaBase):
    id_vin_IoT: int | None = None

class Entrada_Agua(Entrada_AguaBase):
    id_llenado: int | None = None

    class Config:
        orm_mode = True


#------Consumo de agua (Salida) -----#
class Salida_AguaBase(BaseModel):
    cantidad_salida: float | None = None
    Fecha_Hora: str | None = None

class Salida_AguaVin(Salida_AguaBase):
    dispo_IoT: str | None = None

class Salida_AguaCreate(Salida_AguaBase):
    id_vin_IoT: int | None = None

class Salida_Agua(Salida_AguaBase):
    id_consumo: int | None = None

    class Config:
        orm_mode = True


#-----Dispositivos IoT-----#

class IoTBase(BaseModel):
    dispo_IoT: str | None = None

class IoTCreate(IoTBase):
    id_almacenamiento: int | None = None

class IoT(IoTBase):
    id_vin_IoT: int | None = None
    #variables: list[Recepcion_Datos] | None = None
    #entradas: list[Entrada_Agua] | None = None
    #salidas: list[Salida_Agua] | None = None

    class Config:
        orm_mode= True
 


#-------Almacenamientos---------#

class AlmacenamientoBase(BaseModel):
    capacidad_maxima: float | None = None
    ubicacion: str | None = None

class AlmacenamientoCreate(AlmacenamientoBase):
    id_grupo: int | None = None

class Almacenamiento(AlmacenamientoBase):
    id_almacenamiento: int | None = None
    dispo_IoT: IoT | None = None

    class Config:
        orm_mode = True

        
#---------Grupos----------#

class GrupoBase(BaseModel):
    nombre: str | None = None

class GrupoCreate(GrupoBase):
    id_usuario: int | None = None

class Grupo(GrupoBase):
    id_usuario: int | None = None
    id_grupo: int | None = None
    vinculacion: Vinculacion_Grupo | None = None
    almacenamientos: list[Almacenamiento] | None = None

    class Config:
        orm_mode = True



#----------Usuarios----------#

class UsuarioBase(BaseModel):
    usuario: str | None = None


class UserCreate(UsuarioBase):
    password: str | None = None
    id_tipo: int | None = None


class Usuario(UsuarioBase):
    id_usuario: int | None = None
    id_tipo: int | None = None
    grupos: list[Grupo] | None = None

    class Config:
        orm_mode = True






