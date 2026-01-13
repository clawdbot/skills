/**
 * Convex API Client for Plan2Meal
 */

const axios = require('axios');

class ConvexClient {
  constructor(convexUrl, githubToken) {
    this.convexUrl = convexUrl;
    this.githubToken = githubToken;
    this.httpClient = axios.create({
      baseURL: convexUrl,
      headers: {
        'Authorization': `Bearer ${githubToken}`,
        'Content-Type': 'application/json'
      }
    });
  }

  /**
   * Generic query executor
   */
  async query(functionName, args = {}) {
    try {
      const response = await this.httpClient.post('/api/query', {
        functionName,
        args
      });
      return response.data;
    } catch (error) {
      console.error(`Convex query ${functionName} failed:`, error.message);
      throw error;
    }
  }

  /**
   * Generic mutation executor
   */
  async mutation(functionName, args = {}) {
    try {
      const response = await this.httpClient.post('/api/mutation', {
        functionName,
        args
      });
      return response.data;
    } catch (error) {
      console.error(`Convex mutation ${functionName} failed:`, error.message);
      throw error;
    }
  }

  /**
   * Generic action executor
   */
  async action(functionName, args = {}) {
    try {
      const response = await this.httpClient.post('/api/action', {
        functionName,
        args
      });
      return response.data;
    } catch (error) {
      console.error(`Convex action ${functionName} failed:`, error.message);
      throw error;
    }
  }

  // ========== Recipes ==========

  async getAllRecipes() {
    return this.query('recipes.get');
  }

  async getMyRecipes() {
    return this.query('recipes.getMyRecipes');
  }

  async getRecipeById(id) {
    return this.query('recipes.getById', { id });
  }

  async searchRecipes(term) {
    return this.query('recipes.searchMyRecipes', { term });
  }

  async createRecipe(recipeData) {
    return this.mutation('recipes.create', recipeData);
  }

  async updateRecipe(id, updates) {
    return this.mutation('recipes.update', { id, ...updates });
  }

  async deleteRecipe(id) {
    return this.mutation('recipes.remove', { id });
  }

  // ========== Recipe Extraction ==========

  async fetchRecipeMetadata(url) {
    return this.action('recipeExtraction.fetchRecipeMetadata', { url });
  }

  // ========== Grocery Lists ==========

  async getMyLists() {
    return this.query('groceryLists.getMyLists');
  }

  async getListById(id) {
    return this.query('groceryLists.getById', { id });
  }

  async createGroceryList(name, description = '') {
    return this.mutation('groceryLists.create', { name, description });
  }

  async updateGroceryList(id, updates) {
    return this.mutation('groceryLists.update', { id, ...updates });
  }

  async deleteGroceryList(id) {
    return this.mutation('groceryLists.remove', { id });
  }

  async addRecipeToList(groceryListId, recipeId, servings = 1) {
    return this.mutation('groceryLists.addRecipeToList', { groceryListId, recipeId, servings });
  }

  async removeRecipeFromList(groceryListId, recipeId) {
    return this.mutation('groceryLists.removeRecipeFromList', { groceryListId, recipeId });
  }

  async toggleItemCompleted(id, isCompleted) {
    return this.mutation('groceryLists.toggleItemCompleted', { id, isCompleted });
  }

  async addCustomItem(groceryListId, ingredient, quantity, unit) {
    return this.mutation('groceryLists.addCustomItem', { groceryListId, ingredient, quantity, unit });
  }

  async removeItem(id) {
    return this.mutation('groceryLists.removeItem', { id });
  }

  async regenerateListItems(groceryListId) {
    return this.mutation('groceryLists.regenerateItems', { groceryListId });
  }
}

module.exports = ConvexClient;