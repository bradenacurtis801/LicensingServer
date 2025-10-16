import {
  ActivationFormsApi,
  ActivationsApi,
  ApplicationsApi,
  AuthenticationApi,
  CustomersApi,
  DefaultApi,
  LicensesApi,
  ValidationApi,
  Configuration,
} from "@/generated";

// Use relative URLs to leverage Next.js proxy
let apiBaseUrl = process.env.NEXT_PUBLIC_API_URL || "";

// Keep an in-memory token so we can immediately use fresh tokens after login
let currentToken: string | null = null;

// Callback function to get the current token
const getCurrentToken = async (): Promise<string> => {
  const token = typeof window !== 'undefined'
    ? (currentToken ?? localStorage.getItem('auth_token'))
    : currentToken;
  console.log('🔄 getCurrentToken: Current token:', token);
  return token || '';
};

// Create initial configuration
let sharedConfig = new Configuration({
  basePath: apiBaseUrl,
  accessToken: getCurrentToken,
});

// Declare API clients (initially with the default sharedConfig)
export let activationFormsApi = new ActivationFormsApi(sharedConfig);
export let activationsApi = new ActivationsApi(sharedConfig);
export let applicationsApi = new ApplicationsApi(sharedConfig);
export let authenticationApi = new AuthenticationApi(sharedConfig);
export let customersApi = new CustomersApi(sharedConfig);
export let defaultApi = new DefaultApi(sharedConfig);
export let licensesApi = new LicensesApi(sharedConfig);
export let validationApi = new ValidationApi(sharedConfig);

// Function to update the API Base URL dynamically
export const setCurrentClientConfig = (url: string) => {
  apiBaseUrl = url;
  updateApiClients();
};

// Allow setting/clearing the auth token explicitly (e.g., after login/logout)
export const setAuthToken = (token: string | null) => {
  currentToken = token;
  if (typeof window !== 'undefined') {
    if (token) {
      localStorage.setItem('auth_token', token);
    } else {
      localStorage.removeItem('auth_token');
    }
  }
  updateApiClients();
};

// Function to update API clients with current authentication
export const updateApiClients = () => {
  sharedConfig = new Configuration({
    basePath: apiBaseUrl,
    accessToken: getCurrentToken,
  });
  console.log('🔄 New configuration:', sharedConfig);

  // Reinitialize API clients with the updated sharedConfig
  activationFormsApi = new ActivationFormsApi(sharedConfig);
  activationsApi = new ActivationsApi(sharedConfig);
  applicationsApi = new ApplicationsApi(sharedConfig);
  authenticationApi = new AuthenticationApi(sharedConfig);
  customersApi = new CustomersApi(sharedConfig);
  defaultApi = new DefaultApi(sharedConfig);
  licensesApi = new LicensesApi(sharedConfig);
  validationApi = new ValidationApi(sharedConfig);
};
