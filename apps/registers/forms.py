from django import forms
from .models import Register

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Register

        fields = (
            # Juego 1
            "marcador_local_game_1",
            "marcador_visitante_game_1",
            # Juego 2
            "marcador_local_game_2",
            "marcador_visitante_game_2",
            # Juego 3
            "marcador_local_game_3",
            "marcador_visitante_game_3",
            # Juego 4
            "marcador_local_game_4",
            "marcador_visitante_game_4",
            # Juego 5
            "marcador_local_game_5",
            "marcador_visitante_game_5",
            # Juego 6
            "marcador_local_game_6",
            "marcador_visitante_game_6",
            # Juego 7
            "marcador_local_game_7",
            "marcador_visitante_game_7",
            # Juego 8
            "marcador_local_game_8",
            "marcador_visitante_game_8",
            # Juego 9
            "marcador_local_game_9",
            "marcador_visitante_game_9",
            # Juego 10
            "marcador_local_game_10",
            "marcador_visitante_game_10",
            # Juego 11
            "marcador_local_game_11",
            "marcador_visitante_game_11",
            # Juego 12
            "marcador_local_game_12",
            "marcador_visitante_game_12",
            # Juego 13
            "marcador_local_game_13",
            "marcador_visitante_game_13",
            # Juego 14
            "marcador_local_game_14",
            "marcador_visitante_game_14",
            # Juego 15
            "marcador_local_game_15",
            "marcador_visitante_game_15",
            # Juego 16
            "marcador_local_game_16",
            "marcador_visitante_game_16",
            # Juego 17
            "marcador_local_game_17",
            "marcador_visitante_game_17",
            # Juego 18
            "marcador_local_game_18",
            "marcador_visitante_game_18",
            # Juego 19
            "marcador_local_game_19",
            "marcador_visitante_game_19",
            # Juego 20
            "marcador_local_game_20",
            "marcador_visitante_game_20",
            # Juego 21
            "marcador_local_game_21",
            "marcador_visitante_game_21",
            # Juego 22
            "marcador_local_game_22",
            "marcador_visitante_game_22",
            # Juego 23
            "marcador_local_game_23",
            "marcador_visitante_game_23",
            # Juego 24
            "marcador_local_game_24",
            "marcador_visitante_game_24",
            # Juego 25
            "marcador_local_game_25",
            "marcador_visitante_game_25",
            # Juego 26
            "marcador_local_game_26",
            "marcador_visitante_game_26",
            # Juego 27
            "marcador_local_game_27",
            "marcador_visitante_game_27",
            # Juego 28
            "marcador_local_game_28",
            "marcador_visitante_game_28",
            # Juego 29
            "marcador_local_game_29",
            "marcador_visitante_game_29",
            # Juego 30
            "marcador_local_game_30",
            "marcador_visitante_game_30",
            # Juego 31
            "marcador_local_game_31",
            "marcador_visitante_game_31",
            # Juego 32
            "marcador_local_game_32",
            "marcador_visitante_game_32",
            # Juego 33
            "marcador_local_game_33",
            "marcador_visitante_game_33",
            # Juego 34
            "marcador_local_game_34",
            "marcador_visitante_game_34",
            # Juego 35
            "marcador_local_game_35",
            "marcador_visitante_game_35",
            # Juego 36
            "marcador_local_game_36",
            "marcador_visitante_game_36",
            # Juego 37
            "marcador_local_game_37",
            "marcador_visitante_game_37",
            # Juego 38
            "marcador_local_game_38",
            "marcador_visitante_game_38",
            # Juego 39
            "marcador_local_game_39",
            "marcador_visitante_game_39",
            # Juego 40
            "marcador_local_game_40",
            "marcador_visitante_game_40",
            # Juego 41
            "marcador_local_game_41",
            "marcador_visitante_game_41",
            # Juego 42
            "marcador_local_game_42",
            "marcador_visitante_game_42",
            # Juego 43
            "marcador_local_game_43",
            "marcador_visitante_game_43",
            # Juego 44
            "marcador_local_game_44",
            "marcador_visitante_game_44",
            # Juego 45
            "marcador_local_game_45",
            "marcador_visitante_game_45",
            # Juego 46
            "marcador_local_game_46",
            "marcador_visitante_game_46",
            # Juego 47
            "marcador_local_game_47",
            "marcador_visitante_game_47",
            # Juego 48
            "marcador_local_game_48",
            "marcador_visitante_game_48",
            # Juego 49
            "marcador_local_game_49",
            "marcador_visitante_game_49",
            # Juego 50
            "marcador_local_game_50",
            "marcador_visitante_game_50",
            # Juego 51
            "marcador_local_game_51",
            "marcador_visitante_game_51",
            # Juego 52
            "marcador_local_game_52",
            "marcador_visitante_game_52",
            # Juego 53
            "marcador_local_game_53",
            "marcador_visitante_game_53",
            # Juego 54
            "marcador_local_game_54",
            "marcador_visitante_game_54",
            # Juego 55
            "marcador_local_game_55",
            "marcador_visitante_game_55",
            # Juego 56
            "marcador_local_game_56",
            "marcador_visitante_game_56",
            # Juego 57
            "marcador_local_game_57",
            "marcador_visitante_game_57",
            # Juego 58
            "marcador_local_game_58",
            "marcador_visitante_game_58",
            # Juego 59
            "marcador_local_game_59",
            "marcador_visitante_game_59",
            # Juego 60
            "marcador_local_game_60",
            "marcador_visitante_game_60",
            # Juego 61
            "marcador_local_game_61",
            "marcador_visitante_game_61",
            # Juego 62
            "marcador_local_game_62",
            "marcador_visitante_game_62",
            # Juego 63
            "marcador_local_game_63",
            "marcador_visitante_game_63",
            # Juego 64
            "marcador_local_game_64",
            "marcador_visitante_game_64",
            # Juego 65
            "marcador_local_game_65",
            "marcador_visitante_game_65",
            # Juego 66
            "marcador_local_game_66",
            "marcador_visitante_game_66",
            # Juego 67
            "marcador_local_game_67",
            "marcador_visitante_game_67",
            # Juego 68
            "marcador_local_game_68",
            "marcador_visitante_game_68",
            # Juego 69
            "marcador_local_game_69",
            "marcador_visitante_game_69",
            # Juego 70
            "marcador_local_game_70",
            "marcador_visitante_game_70",
            # Juego 71
            "marcador_local_game_71",
            "marcador_visitante_game_71",
            # Juego 72
            "marcador_local_game_72",
            "marcador_visitante_game_72",
        )

        # Excluimos el campo usuario_registro para que no se muestre en el formulario
        exclude = ['usuario_registro']


class UpdatePointsForm(forms.ModelForm):
    class Meta:
        model = Register

        fields = (
            "puntos_game_1",
            "puntos_game_2",
            "puntos_game_3",
            "puntos_game_4",
            "puntos_game_5",
            "puntos_game_6",
            "puntos_game_7",
            "puntos_game_8",
            "puntos_game_9",
            "puntos_game_10",
            "puntos_game_11",
            "puntos_game_12",
            "puntos_game_13",
            "puntos_game_14",
            "puntos_game_15",
            "puntos_game_16",
            "puntos_game_17",
            "puntos_game_18",
            "puntos_game_19",
            "puntos_game_20",
            "puntos_game_21",
            "puntos_game_22",
            "puntos_game_23",
            "puntos_game_24",
            "puntos_game_25",
            "puntos_game_26",
            "puntos_game_27",
            "puntos_game_28",
            "puntos_game_29",
            "puntos_game_30",
            "puntos_game_31",
            "puntos_game_32",
            "puntos_game_33",
            "puntos_game_34",
            "puntos_game_35",
            "puntos_game_36",
            "puntos_game_37",
            "puntos_game_38",
            "puntos_game_39",
            "puntos_game_40",
            "puntos_game_41",
            "puntos_game_42",
            "puntos_game_43",
            "puntos_game_44",
            "puntos_game_45",
            "puntos_game_46",
            "puntos_game_47",
            "puntos_game_48",
            "puntos_game_49",
            "puntos_game_50",
            "puntos_game_51",
            "puntos_game_52",
            "puntos_game_53",
            "puntos_game_54",
            "puntos_game_55",
            "puntos_game_56",
            "puntos_game_57",
            "puntos_game_58",
            "puntos_game_59",
            "puntos_game_60",
            "puntos_game_61",
            "puntos_game_62",
            "puntos_game_63",
            "puntos_game_64",
            "puntos_game_65",
            "puntos_game_66",
            "puntos_game_67",
            "puntos_game_68",
            "puntos_game_69",
            "puntos_game_70",
            "puntos_game_71",
            "puntos_game_72",
        )

        # Excluimos el campo usuario_registro para que no se muestre en el formulario
        exclude = ['usuario_registro']
