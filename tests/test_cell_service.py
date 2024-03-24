from unittest.mock import patch, MagicMock

import pytest

from models.cell import CreateCellDto
from repositories import CellRepository
from schemas.cell import Cell
from services import CellService
from test_config import mock_db_session


@pytest.fixture
def mock_service(mock_db_session):
    cell_repo = CellRepository(mock_db_session)
    return CellService(mock_db_session, cell_repo)


def test_create_cell_raise_error_when_no_parent(mock_service):
    mock_repo = MagicMock(spec=CellRepository)
    with patch.object(mock_service, 'cell_repo', mock_repo):
        mock_repo.find_by.side_effect = [None, None]
        data = CreateCellDto(**{
            'sheet_id': 1,
            'goal': 'test',
            'color': '#fff',
            'depth': 2,
            'order': 3,
            'parent_order': 3
        })
        try:
            mock_service.create_cell(data)
            assert False
        except ValueError:
            assert True
        assert mock_repo.find_by.call_count == 2


def test_create_cell_raise_error_already_exists(mock_service):
    mock_repo = MagicMock(spec=CellRepository)
    with patch.object(mock_service, 'cell_repo', mock_repo):
        mock_repo.find_by.side_effect = [Cell(depth=2,order=3)]
        data = CreateCellDto(**{
            'sheet_id': 1,
            'goal': 'test',
            'color': '#fff',
            'depth': 2,
            'order': 3,
            'parent_order': 3
        })
        try:
            mock_service.create_cell(data)
            assert False
        except ValueError:
            assert True
        assert mock_repo.find_by.call_count == 1