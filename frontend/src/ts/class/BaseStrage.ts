type StoreListener<K> = (state: K) => void;

export default class BaseStorage<K extends object>
{
    private readonly listeners = new Set<StoreListener<K>>();

    public store: K;

    public readonly clearStore: () => void;
    
    constructor (
        private readonly keyStorage: string,
        private readonly initialState: K
    ) {
        const baseState = this.loadFromStorage();

        this.store = new Proxy(baseState, {
            set: (target, property, value) => {
            
                Reflect.set(target, property, value);
            
                this.saveToStorage(target);
            
                this.listeners.forEach(
                    listener => listener(this.store)
                );
            
                return true;
            }
        });

        this.clearStore = () => {
        
            localStorage.removeItem(this.keyStorage);
        
            Object.keys(baseState).forEach(
                key => delete baseState[key as keyof K]
            );
        
            Object.assign(
                baseState,
                structuredClone(this.initialState)
            );
        
            this.listeners.forEach(
                listener => listener(this.store)
            );
        };
    }

    private loadFromStorage(): K {
        const data = localStorage.getItem(this.keyStorage);
        return data
            ? JSON.parse(data) as K
            : structuredClone(this.initialState);
    }

    private saveToStorage(state: K): void {
        localStorage.setItem(
            this.keyStorage,
            JSON.stringify(state)
        );
    }

    public subscribe(listener: StoreListener<K>): () => void {

        this.listeners.add(listener);

        listener(this.store);

        return () => {
            this.listeners.delete(listener);
        };
    }
}