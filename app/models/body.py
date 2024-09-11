from typing import Any

import fastapi

from .models import *

TX = (
    TxInvokeV0
    | TxInvokeV1
    | TxInvokeV3
    | TxDeclareV1
    | TxDeclareV2
    | TxDeclareV3
    | TxDeployV1
    | TxDeployV3
)


def doc_tx_invoke_v1() -> dict[str, Any]:
    tx = TxInvokeV1(
        sender_address="0x0",
        calldata=["0x0"],
        max_fee="0x0",
        signature="0x0",
        nonce="0x0",
    )

    return tx.model_dump()


class _BodyCall(pydantic.BaseModel):
    contract_address: FieldHex
    entry_point_selector: FieldHex
    calldata: list[FieldHex] = []


Call = Annotated[_BodyCall, fastapi.Body(include_in_schema=False)]


class _BodyEstimateFee(pydantic.BaseModel):
    request: Annotated[
        TX,
        fastapi.Body(
            description=(
                "a sequence of transactions to estimate, running each "
                "transaction on the state resulting from applying all the "
                "previous ones"
            ),
            examples=[doc_tx_invoke_v1()],
        ),
    ]
    simulation_flags: Annotated[
        list[SimulationFlags],
        fastapi.Body(
            description=(
                "describes what parts of the transaction should be executed"
            )
        ),
    ]


EstimateFee = Annotated[_BodyEstimateFee, fastapi.Body(include_in_schema=False)]


class _BodyEstimateMessageFee(pydantic.BaseModel):
    from_address: Annotated[
        FieldHex,
        pydantic.Field(
            title="Ethereum address",
            description="The address of the L1 contract sending the message",
        ),
    ]
    to_address: Annotated[
        FieldHex,
        pydantic.Field(
            title="Starknet address",
            description="The target L2 address the message is sent to",
        ),
    ]
    entry_point_selector: Annotated[
        FieldHex,
        pydantic.Field(
            description=(
                "Entry point in the L1 contract used to send the message"
            )
        ),
    ]
    payload: Annotated[
        list[FieldHex],
        pydantic.Field(
            description=(
                "The message payload being sent to an address on Starknet"
            )
        ),
    ]


EstimateMessageFee = Annotated[
    _BodyEstimateMessageFee, fastapi.Body(include_in_schema=False)
]
