/**
 * GitHub OAuth Helper
 */

const axios = require('axios');

class GitHubOAuth {
  constructor(clientId, clientSecret, clawdbotUrl) {
    this.clientId = clientId;
    this.clientSecret = clientSecret;
    this.clawdbotUrl = clawdbotUrl;
  }

  /**
   * Generate OAuth authorization URL
   */
  getAuthUrl(state) {
    const params = new URLSearchParams({
      client_id: this.clientId,
      redirect_uri: `${this.clawdbotUrl}/oauth/github/callback`,
      scope: 'read:user user:email',
      state,
      allow_signup: false
    });
    return `https://github.com/login/oauth/authorize?${params.toString()}`;
  }

  /**
   * Exchange code for access token
   */
  async exchangeCode(code) {
    try {
      const response = await axios.post('https://github.com/login/oauth/access_token', {
        client_id: this.clientId,
        client_secret: this.clientSecret,
        code,
        accept: 'json'
      });

      if (response.data.error) {
        throw new Error(response.data.error_description || response.data.error);
      }

      return response.data.access_token;
    } catch (error) {
      console.error('GitHub OAuth token exchange failed:', error.message);
      throw error;
    }
  }

  /**
   * Get user info from GitHub
   */
  async getUserInfo(accessToken) {
    try {
      const response = await axios.get('https://api.github.com/user', {
        headers: {
          Authorization: `Bearer ${accessToken}`,
          Accept: 'application/vnd.github.v3+json'
        }
      });

      return {
        id: response.data.id,
        login: response.data.login,
        name: response.data.name,
        email: response.data.email,
        avatar_url: response.data.avatar_url
      };
    } catch (error) {
      console.error('GitHub user info fetch failed:', error.message);
      throw error;
    }
  }

  /**
   * Check if user is authenticated (validate token)
   */
  async validateToken(accessToken) {
    try {
      await this.getUserInfo(accessToken);
      return true;
    } catch {
      return false;
    }
  }
}

module.exports = GitHubOAuth;