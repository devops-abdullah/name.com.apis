import axios, { AxiosInstance } from 'axios'

class APIClient {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: 'http://localhost:8000',
      headers: {
        'Content-Type': 'application/json'
      }
    })

    // Add token to requests
    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('access_token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    })

    // Handle errors
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('access_token')
          window.location.href = '/login'
        }
        return Promise.reject(error)
      }
    )
  }

  // Auth endpoints
  register(username: string, email: string, password: string, full_name?: string) {
    return this.client.post('/api/auth/register', {
      username,
      email,
      password,
      full_name
    })
  }

  login(username: string, password: string) {
    return this.client.post('/api/auth/login', {
      username,
      password
    })
  }

  logout() {
    return this.client.post('/api/auth/logout')
  }

  getCurrentUser() {
    return this.client.get('/api/auth/me')
  }

  // Teams endpoints
  getTeams() {
    return this.client.get('/api/teams')
  }

  getTeam(teamId: number) {
    return this.client.get(`/api/teams/${teamId}`)
  }

  createTeam(name: string, description?: string) {
    return this.client.post('/api/teams', { name, description })
  }

  updateTeam(teamId: number, name?: string, description?: string) {
    return this.client.put(`/api/teams/${teamId}`, { name, description })
  }

  deleteTeam(teamId: number) {
    return this.client.delete(`/api/teams/${teamId}`)
  }

  addTeamMember(teamId: number, userId: number, role: string = 'member') {
    return this.client.post(`/api/teams/${teamId}/members/${userId}`, { role })
  }

  removeTeamMember(teamId: number, userId: number) {
    return this.client.delete(`/api/teams/${teamId}/members/${userId}`)
  }

  // Domains endpoints
  getDomains() {
    return this.client.get('/api/domains')
  }

  getDomain(domainName: string) {
    return this.client.get(`/api/domains/${domainName}`)
  }

  getDomainRecords(domainName: string) {
    return this.client.get(`/api/domains/${domainName}/records`)
  }

  createDNSRecord(domainName: string, name: string, type: string, content: string, ttl?: number, priority?: number) {
    return this.client.post(`/api/domains/${domainName}/records`, {
      name,
      type,
      content,
      ttl,
      priority
    })
  }

  updateDNSRecord(domainName: string, recordId: number, content?: string, ttl?: number, priority?: number) {
    return this.client.put(`/api/domains/${domainName}/records/${recordId}`, {
      content,
      ttl,
      priority
    })
  }

  deleteDNSRecord(domainName: string, recordId: number) {
    return this.client.delete(`/api/domains/${domainName}/records/${recordId}`)
  }
}

export default new APIClient()
