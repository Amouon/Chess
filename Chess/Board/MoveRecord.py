from dataclasses import dataclass
from typing import Tuple, Optional

from Chess.Pieces.piece import Piece


@dataclass
class MoveRecord:
    start_row: int
    start_col: int
    end_row: int
    end_col: int
    moved_piece: "Piece"
    captured_piece: Optional["Piece"]
    old_castling_rights: Tuple[bool, bool]  # e.g. (king_side, queen_side)
    old_en_passant_square: Optional[Tuple[int, int]]
    old_half_moves: int
    old_turn: str