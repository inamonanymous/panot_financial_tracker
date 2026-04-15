class GetSavingGoalDetailsUseCase:
    """Retrieve a saving goal and its transaction history for a user."""

    def __init__(self, unit_of_work):
        self.uow = unit_of_work

    def execute(self, goal_id: int, user_id: int):
        """
        Get saving goal details and payment history.

        Args:
            goal_id: ID of the saving goal
            user_id: ID of the user (owner)

        Returns:
            dict with 'goal' and 'payments' keys
        """
        goal = self.uow.saving_goals.get_by_id_and_user_id(goal_id, user_id)
        if goal is None:
            raise Exception("Saving goal not found")

        payments = self.uow.saving_transactions.get_all_by_goal_id(goal_id)

        # Attach progress data to the goal for the presentation layer
        goal.progress_percentage = self.uow.saving_goals.calculate_progress_percentage(
            goal_id,
            goal.target_amount,
        )
        print(f"Progress percentage: {goal.progress_percentage}%")
        
        return {
            'goal': goal,
            'payments': payments if payments else []
        }
