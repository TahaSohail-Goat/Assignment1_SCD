export interface paths {
    "/api/complaints": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations["listComplaints"];
        put?: never;
        post: operations["createComplaint"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/complaints/{id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations["getComplaint"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/complaints/{id}/status": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch: operations["updateStatus"];
        trace?: never;
    };
    "/api/stats": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations["getStats"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/meta/providers": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations["getProviders"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
}
export type webhooks = Record<string, never>;
export interface components {
    schemas: {
        /** @enum {string} */
        Category: "water" | "electricity" | "sanitation" | "roads" | "streetlights" | "other";
        /** @enum {string} */
        Priority: "high" | "normal" | "low";
        /** @enum {string} */
        Status: "open" | "in_progress" | "resolved" | "rejected";
        ComplaintCreate: {
            text: string;
            location: string;
            reporter_contact?: string | null;
        };
        Complaint: {
            /** Format: uuid */
            id: string;
            text: string;
            location: string;
            reporter_contact: string | null;
            category: components["schemas"]["Category"];
            priority: components["schemas"]["Priority"];
            status: components["schemas"]["Status"];
            ai_summary: string | null;
            triaged_by: string;
            triage_latency_ms: number;
            /** Format: date-time */
            created_at: string;
            /** Format: date-time */
            updated_at: string;
        };
        StatusUpdate: {
            status: components["schemas"]["Status"];
        };
        ComplaintPage: {
            items: components["schemas"]["Complaint"][];
            total: number;
            page: number;
            page_size: number;
        };
        Stats: {
            total: number;
            by_category: {
                [key: string]: number;
            };
            by_priority: {
                [key: string]: number;
            };
        };
        TriageOutcome: {
            /** Format: uuid */
            complaint_id: string;
            provider: string;
            latency_ms: number;
            fallback: boolean;
            /** Format: date-time */
            at: string;
        };
        ProvidersMeta: {
            active_provider: string;
            recent: components["schemas"]["TriageOutcome"][];
        };
        ApiError: {
            error: {
                code: string;
                message: string;
                details?: {
                    [key: string]: unknown;
                }[];
            };
        };
    };
    responses: {
        /** @description API error */
        Error: {
            headers: {
                [name: string]: unknown;
            };
            content: {
                "application/json": components["schemas"]["ApiError"];
            };
        };
    };
    parameters: never;
    requestBodies: never;
    headers: never;
    pathItems: never;
}
export type $defs = Record<string, never>;
export interface operations {
    listComplaints: {
        parameters: {
            query?: {
                page?: number;
                page_size?: number;
                category?: components["schemas"]["Category"];
                priority?: components["schemas"]["Priority"];
                status?: components["schemas"]["Status"];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Page */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ComplaintPage"];
                };
            };
            400: components["responses"]["Error"];
        };
    };
    createComplaint: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ComplaintCreate"];
            };
        };
        responses: {
            /** @description Created */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Complaint"];
                };
            };
            400: components["responses"]["Error"];
            429: components["responses"]["Error"];
        };
    };
    getComplaint: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                id: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Complaint */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Complaint"];
                };
            };
            404: components["responses"]["Error"];
        };
    };
    updateStatus: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                id: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["StatusUpdate"];
            };
        };
        responses: {
            /** @description Updated */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Complaint"];
                };
            };
            400: components["responses"]["Error"];
            404: components["responses"]["Error"];
            409: components["responses"]["Error"];
        };
    };
    getStats: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Statistics */
            200: {
                headers: {
                    "X-Cache"?: "HIT" | "MISS";
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Stats"];
                };
            };
        };
    };
    getProviders: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Providers */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ProvidersMeta"];
                };
            };
        };
    };
}
