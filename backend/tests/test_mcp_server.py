from app.mcp_server import mcp

def test_get_rank_data_tool_found():
    """Test the get_rank_data tool when data is found."""
    tool = mcp._tool_manager.get_tool("get_rank_data")
    result = tool.fn(rank_name="Captain")
    assert result["rank"] == "Captain"
    assert "responsibilities" in result
    assert isinstance(result["responsibilities"], list)

def test_get_rank_data_tool_not_found():
    """Test the get_rank_data tool when data is not found."""
    tool = mcp._tool_manager.get_tool("get_rank_data")
    result = tool.fn(rank_name="General")
    assert result == {}

def test_get_mosid_data_tool_found():
    """Test the get_mosid_data tool when data is found."""
    tool = mcp._tool_manager.get_tool("get_mosid_data")
    result = tool.fn(mosid_code="00005")
    assert result["mosid"] == "00005"
    assert "title" in result
    assert "equivalencies" in result
    assert isinstance(result["equivalencies"], list)
    assert len(result["equivalencies"]) > 0

def test_get_mosid_data_tool_not_found():
    """Test the get_mosid_data tool when data is not found."""
    tool = mcp._tool_manager.get_tool("get_mosid_data")
    result = tool.fn(mosid_code="invalid-mosid")
    assert result == {}

def test_get_mosid_data_batch_tool():
    """Test the get_mosid_data_batch tool."""
    tool = mcp._tool_manager.get_tool("get_mosid_data_batch")
    result = tool.fn(mosid_codes=["00005", "00008"])
    assert "00005" in result
    assert "00008" in result
    assert "equivalencies" in result["00005"]
    assert "equivalencies" in result["00008"]
