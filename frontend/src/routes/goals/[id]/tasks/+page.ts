import type { PageLoad } from "./$types";
import { getGoal } from "$lib/api/goals";

export const load: PageLoad = async ({ params }) => {
	return await getGoal(params.id);
};
