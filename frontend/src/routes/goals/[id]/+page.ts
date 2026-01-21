import type { PageLoad } from "./$types";
import { getGoal } from "$lib/api/goals";
import { takeGoalCache } from "$lib/stores/goalCache";
import { browser } from "$app/environment";

export const load: PageLoad = async ({ params }) => {
	if (browser) {
		const cached = takeGoalCache(params.id);
		if (cached) return cached;
	}

	return await getGoal(params.id);
};
