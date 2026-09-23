from crewai.tools import tool

from memory import save_memory, get_memories, search_memories


@tool("Save Student Memory")
def save_student_memory(memory: str) -> str:
    """
    Save useful information about the student's
    learning preferences, goals, subjects, or progress.
    """

    save_memory(memory)

    return f"Memory saved successfully: {memory}"


@tool("Recall Student Memory")
def recall_student_memory(keyword: str) -> str:
    """
    Search the student's previous memories using a keyword.
    """

    memories = search_memories(keyword)

    if not memories:
        return "No relevant memories were found."

    return "\n".join(
        f"- {memory}"
        for memory in memories
    )


@tool("Get Recent Memories")
def get_recent_memories() -> str:
    """
    Retrieve the student's most recent memories.
    """

    memories = get_memories()

    if not memories:
        return "There are no saved memories yet."

    return "\n".join(
        f"- {memory}"
        for memory in memories
    )


@tool("Calculator")
def calculator(expression: str) -> str:
    """
    Perform a basic mathematical calculation.

    Example:
    25 * 4
    """

    try:
        allowed_characters = "0123456789+-*/().% "

        if not all(
            character in allowed_characters
            for character in expression
        ):
            return "Invalid mathematical expression."

        result = eval(expression, {"__builtins__": {}})

        return f"Result: {result}"

    except Exception:
        return "I could not calculate that expression."
