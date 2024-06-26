from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from errors.exceptions import UnauthorizedException, EntityNotFoundException
from models.cell import UpdateCellDto, GetCellDto, GetCellWithTodosDto
from repositories import SheetRepository
from repositories.cell import CellRepository
from schemas import Sheet
from schemas.cell import Cell
from schemas.todo import Todo
from transaction import Transaction


class CellService:
    cell_repo: CellRepository
    sheet_repo: SheetRepository
    db: Session

    def __init__(self,
                 db: Annotated[Session, Depends(get_db)],
                 cell_repo: Annotated[CellRepository, Depends()],
                 sheet_repo: Annotated[SheetRepository, Depends()],
                 transaction: Annotated[Transaction, Depends()]
                 ):
        self.db = db
        self.cell_repo = cell_repo
        self.sheet_repo = sheet_repo
        self.transaction = transaction

    # def create_cell(self, dto: CreateCellDto, user_id: int = 1):
    #     cell = Cell(
    #         step=dto.step,
    #         order=dto.order,
    #         goal=dto.goal,
    #         sheet_id=dto.sheet_id,
    #         color=dto.color
    #     )
    #
    #     sheet = self.sheet_repo.find_by_id(dto.sheet_id)
    #     if not sheet:
    #         raise ValueError("sheet not found")
    #
    #     if sheet.owner_id != user_id:
    #         raise UnauthorizedException()
    #
    #     if prev_cell := self.cell_repo.find_by(step=dto.step, order=dto.order, sheet_id=dto.sheet_id):
    #         raise ValueError(f"Cell with step {dto.step} and order {dto.order} has been already existed")
    #
    #     if dto.step > 1:
    #         parent_cells = self.cell_repo.find_by(step=dto.step - 1, sheet_id=dto.sheet_id,
    #                                               order=dto.parent_order)
    #         if not parent_cells:
    #             raise ValueError("Parent cell not found")
    #         parent_cell = parent_cells.pop()
    #
    #         parent_cell.children.append(cell)
    #         self.db.add(parent_cell)
    #     else:
    #         self.db.add(cell)
    #     self.db.commit()
    #     return cell
    def delete_cell(self, user_id: int, cell_id: int) -> GetCellWithTodosDto:
        cell = self.cell_repo.find_by_id(cell_id)
        if not cell:
            raise EntityNotFoundException(Cell, id=cell_id)

        if cell.sheet.owner_id != user_id:
            raise UnauthorizedException()

        with self.transaction:
            cell.color = None
            cell.goal = None
            cell.todos = []
            cell.is_completed = False
            if cell.step == 2:
                for child in cell.children:
                    child.color = None
                    child.goal = None
                    child.todos = []
                    child.is_completed = False

        self.cell_repo.create_or_update(cell)

        return GetCellWithTodosDto.from_orm(cell)

    def update_cell(self, dto: UpdateCellDto, user_id: int, cell_id: int) -> GetCellWithTodosDto:
        cell = self.cell_repo.find_by_id(cell_id)
        if not cell:
            raise EntityNotFoundException(Cell, id=cell_id)

        if cell.sheet.owner_id != user_id:
            raise UnauthorizedException()
        with self.transaction:
            cell.color = dto.color if dto.color else cell.color
            cell.goal = dto.goal if dto.goal else cell.goal
            cell.is_completed = dto.is_completed if dto.is_completed is not None else cell.is_completed
            cell.todos = [Todo(owner_id=user_id, content=todo) for todo in dto.todos]
            self.cell_repo.create_or_update(cell)
        return GetCellWithTodosDto.from_orm(cell)

    def get_by_id(self, user_id: int, cell_id: int) -> GetCellWithTodosDto:
        cell = self.cell_repo.find_by_id(cell_id)
        if not cell:
            raise EntityNotFoundException(Cell, id=cell_id)

        if cell.sheet.owner_id != user_id:
            raise UnauthorizedException()

        return GetCellWithTodosDto.from_orm(cell)

    def get_by_sheet_id_and_depth_and_parent_order(self,
                                                   user_id: int,
                                                   sheet_id: int,
                                                   depth: int,
                                                   parent_order: int) -> list[GetCellDto]:

        """
        depth: 1: 정중앙 9개 셀, 2: 정중앙 주위의 9개 셀
        parent_order: 0: 좌상단, 1: 상단, 2: 우상단, 3: 좌측, 4: 우측, 5:좌하단, 6: 하단, 7: 우하단
        """
        sheet = self.sheet_repo.find_by_id(sheet_id)
        if not sheet:
            raise EntityNotFoundException(Sheet, id=sheet_id)
        if sheet.owner_id != user_id:
            raise UnauthorizedException()

        parent_cell = self.cell_repo.find_by(sheet_id=sheet_id, step=depth, order=parent_order)
        if not parent_cell:
            raise ValueError(
                f"Invalid arguments sheet_id, depth, and parent_order: {sheet_id}, {depth}, {parent_order}")
        parent_cell = parent_cell.pop()
        result = [GetCellDto.from_orm(child) for child in parent_cell.children]
        result.insert(4, GetCellDto.from_orm(parent_cell))
        return result

    def get_children_cells_by_id(self, user_id, cell_id) -> list[GetCellDto]:
        cell = self.cell_repo.find_by_id(cell_id)
        if not cell:
            raise EntityNotFoundException(Cell, id=cell_id)

        if cell.sheet.owner_id != user_id:
            raise UnauthorizedException()

        result = [GetCellDto.from_orm(child) for child in cell.children]
        result.insert(4, GetCellDto.from_orm(cell))

        return result
