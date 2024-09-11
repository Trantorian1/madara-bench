from enum import Enum
from typing import Annotated

import pydantic

REGEX_HEX: str = "^0x[a-fA-F0-9]+$"
REGEX_BASE_64: str = "^0x[a-zA-Z0-9]+$"

HexField = Annotated[str, pydantic.Field(pattern=REGEX_HEX)]
Base64Field = Annotated[str, pydantic.Field(pattern=REGEX_BASE_64)]


class NodeName(str, Enum):
    madara = "madara"


class BlockTag(str, Enum):
    latest = "latest"
    pending = "pending"


class CallRequest(pydantic.BaseModel):
    contract_address: HexField
    entry_point_selector: HexField
    calldata: list[HexField] = []


class TxType(str, Enum):
    INVOKE = "INVOKE"
    DECLARE = "DECLARE"
    DEPLOY_ACCOUNT = "DEPLOY_ACCOUNT"


class TxVersion(int, Enum):
    V0 = 0
    V1 = 1
    V2 = 2
    V3 = 3


class TxInvokeV0(pydantic.BaseModel):
    type: TxType = TxType.INVOKE
    mas_fee: HexField
    version: TxVersion = TxVersion.V0
    signature: list[HexField]
    contract_address: HexField
    entry_point_selector: HexField
    calldata: list[HexField] = []

    model_config = {"json_schema_extra": {"deprecated": True}}


class TxInvokeV1(pydantic.BaseModel):
    type: TxType = TxType.INVOKE
    max_fee: HexField
    version: TxVersion = TxVersion.V1
    signature: list[HexField]
    nonce: HexField
    sender_address: HexField
    entry_point_selector: HexField
    calldata: list[HexField] = []


class ResourceBoundsGas(pydantic.BaseModel):
    max_amount: HexField
    max_price_per_unit: HexField


class ResourceBounds(pydantic.BaseModel):
    l1_gas: ResourceBoundsGas
    l2_gas: ResourceBoundsGas


class DaMode(str, Enum):
    L1 = "L1"
    L2 = "L2"


class TxInvokeV3(pydantic.BaseModel):
    type: Annotated[
        TxType,
        pydantic.Field(
            description=(
                "The transaction type, will default to INVOKE for "
                "invoke transactions. You should not pass any other value "
                "than this"
            )
        ),
    ] = TxType.INVOKE
    version: Annotated[
        TxVersion,
        pydantic.Field(
            description=(
                "The transaction version, will default to V3. You "
                "should not pass any other value than this."
            )
        ),
    ] = TxVersion.V3
    signature: Annotated[
        list[HexField], pydantic.Field(description="A transaction signature")
    ]
    nonce: Annotated[
        HexField,
        pydantic.Field(description="Transaction nonce, avoids replay attacks"),
    ]
    sender_address: Annotated[
        HexField,
        pydantic.Field(
            description=(
                "The address of the account contract sending the invoke "
                "transaction"
            )
        ),
    ]
    calldata: Annotated[
        list[HexField],
        pydantic.Field(
            description=(
                "The data expected by the account's `execute` function (in "
                "most usecases, this includes the called contract address and "
                "a function selector)"
            )
        ),
    ] = []
    resource_bounds: Annotated[
        ResourceBounds,
        pydantic.Field(
            description=(
                "Resource bounds for the transaction execution, allow you to "
                "specify a max gas price for l1 and l2"
            )
        ),
    ]
    tip: Annotated[
        HexField,
        pydantic.Field(
            description=(
                "The tip for the transaction. A higher tip means your "
                "transaction should be processed faster."
            )
        ),
    ]
    paymaster_data: Annotated[
        list[HexField],
        pydantic.Field(
            description=(
                "Data needed to allow the paymaster to pay for the "
                "transaction in native tokens"
            )
        ),
    ]
    acount_deployment_data: Annotated[
        list[HexField],
        pydantic.Field(
            description=(
                "data needed to deploy the account contract from "
                "which this tx will be initiated"
            )
        ),
    ]
    nonce_data_availability_mode: Annotated[
        DaMode,
        pydantic.Field(
            description=(
                "The storage domain of the account's nonce (an account has a "
                "nonce per DA mode)"
            )
        ),
    ]
    fee_data_availability_mode: Annotated[
        DaMode,
        pydantic.Field(
            description=(
                "The storage domain of the account's balance from "
                "which fee will be charged"
            )
        ),
    ]


class CairoV1EntryPoint(pydantic.BaseModel):
    offset: Annotated[
        HexField,
        pydantic.Field(
            description="The offset of the entry point in the program",
            deprecated=True,
        ),
    ]
    selector: Annotated[
        HexField,
        pydantic.Field(
            description=(
                "A unique identifier of the entry point (function) in "
                "the program"
            ),
            deprecated=True,
        ),
    ]


class CairoV1EntryPointByType(pydantic.BaseModel):
    CONSTRUCTOR: Annotated[
        list[CairoV1EntryPoint],
        pydantic.Field(description="Deprecated constructor", deprecated=True),
    ]
    EXTERNAL: Annotated[
        list[CairoV1EntryPoint],
        pydantic.Field(description="Deprecated external", deprecated=True),
    ]
    L1_HANDLER: Annotated[
        list[CairoV1EntryPoint],
        pydantic.Field(
            description="Deprecated Cairo entry point", deprecated=True
        ),
    ]


class CairoV1ABIFunctionType(str, Enum):
    function = "function"
    l1_handler = "l1_handler"
    constructor = "constructor"


class CairoV1TypedParameter(pydantic.BaseModel):
    name: Annotated[str, pydantic.Field(description="Parameter name")]
    type: Annotated[str, pydantic.Field(description="Parameter type")]


class CairoV1StateMutability(str, Enum):
    view = "view"


class CairoV1ABIEntryFunction(pydantic.BaseModel):
    type: Annotated[
        CairoV1ABIFunctionType, pydantic.Field(description="Function ABI type")
    ]
    name: Annotated[str, pydantic.Field(description="Function name")]
    inputs: Annotated[
        list[CairoV1TypedParameter],
        pydantic.Field(description="Function input typed parameters"),
    ]
    output: Annotated[
        list[CairoV1TypedParameter],
        pydantic.Field(description="Function output typed parameters"),
    ]
    stateMutability: Annotated[
        CairoV1StateMutability,
        pydantic.Field(
            description=(
                "Defines if a function is allowed to mutate state or "
                "if it must be pure"
            )
        ),
    ]


class CairoV1ABIEventType(str, Enum):
    event = "event"


class CairoV1ABIEntryEvent(pydantic.BaseModel):
    type: Annotated[
        CairoV1ABIEventType,
        pydantic.Field(
            description=(
                "Event ABI type. This defaults to 'event' and is only used to "
                "differentiate from the other ABI entry types"
            )
        ),
    ] = CairoV1ABIEventType.event
    name: Annotated[str, pydantic.Field(description="Event name")]
    keys: Annotated[
        list[CairoV1TypedParameter],
        pydantic.Field(description="Event keys used to query this event"),
    ]
    data: Annotated[
        list[CairoV1TypedParameter],
        pydantic.Field(description="Data held by the event as typed parameter"),
    ]


class CairoV1ABIStructType(str, Enum):
    struct = "struct"


class CairoV1StructEntryOffset(pydantic.BaseModel):
    offset: Annotated[
        int, pydantic.Field(description="Offset of a property within a struct")
    ]


class CairoV1ABIEntryStruct(pydantic.BaseModel):
    type: Annotated[
        CairoV1ABIStructType,
        pydantic.Field(
            description=(
                "Struct ABI type. This defaults to 'struct' and is only used "
                "to differentiate from the other ABI entry types"
            )
        ),
    ] = CairoV1ABIStructType.struct
    name: Annotated[str, pydantic.Field(description="Struct name")]
    size: Annotated[int, pydantic.Field(description="Struct size")]
    members: Annotated[
        list[CairoV1TypedParameter | CairoV1StructEntryOffset],
        pydantic.Field(
            description=(
                "Struct members. This includes struct properties, as typed "
                "parameters, and the offset to each of these properties."
            )
        ),
    ]


class CairoV1ContractClass(pydantic.BaseModel):
    program: Annotated[
        Base64Field,
        pydantic.Field(
            description="A base64 representation of the compressed program code"
        ),
    ]
    entry_points_by_type: Annotated[
        CairoV1EntryPointByType,
        pydantic.Field(
            description="Deprecated entry point by type", deprecated=True
        ),
    ]
    abit: Annotated[
        list[
            CairoV1ABIEntryFunction
            | CairoV1ABIEntryEvent
            | CairoV1ABIEntryStruct
        ],
        pydantic.Field(
            description="Intermediary program sierra representation"
        ),
    ]


class TxDeclareV1(pydantic.BaseModel):
    type: Annotated[
        TxType,
        pydantic.Field(
            description=(
                "The transaction type, will default to DECLARE for "
                "declare transactions. You should not pass any other value "
                "than this"
            )
        ),
    ] = TxType.DECLARE
    sender_address: Annotated[
        HexField,
        pydantic.Field(
            description=(
                "The address of the account contract sending the declaration "
                "transaction"
            )
        ),
    ]
    max_fee: Annotated[
        HexField,
        pydantic.Field(
            description=(
                "The maximal fee that can be charged for including "
                "the transaction"
            )
        ),
    ]
    version: Annotated[
        TxVersion,
        pydantic.Field(
            description=(
                "The transaction version, will default to V1. You "
                "should not pass any other value than this."
            )
        ),
    ] = TxVersion.V1
    signature: Annotated[
        HexField, pydantic.Field(description="A transaction signature")
    ]
    nonce: Annotated[
        HexField,
        pydantic.Field(description="Transaction nonce, avoids replay attacks"),
    ]
    contract_class: Annotated[
        CairoV1ContractClass,
        pydantic.Field(description="The class to be declared"),
    ]

    model_config = {"json_schema_extra": {"deprecated": True}}


class EstimeFeeRequest(pydantic.BaseModel):
    schema_aliased: Annotated[
        list[TxInvokeV0 | TxInvokeV1 | TxInvokeV3 | TxDeclareV1],
        pydantic.Field(
            alias="schema",
            description="a sequence of transactions to estimate, running each transaction on the state resulting from applying all the previous ones",
        ),
    ]
