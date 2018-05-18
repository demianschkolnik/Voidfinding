typedef struct {
	float x;
	float y;
	int valid;
} Point;

int getPos(int i, int j, int n){
	return i+n*j;
}

float distancia(Point A, Point B){
	return sqrt(pown(B.x-A.x,2)+pown(B.y-A.y,2));
}

kernel void isCore(global const Point* points, global const Point* matriz,global int* resultados, int k, float epsilon, int ancho, ){
	
	int idx = get_global_id(0);
	int nrVec = 0;
	for(int i=0;i<ancho;i++){
		if(distancia(points[idx],matriz[getPos(idx,i,ancho)]) <= epsilon) nrVec++;
		if(nrVec>=k) {
			resultados[idx] = 1;
			return;
		}

	}
	resultados[idx] = 0;

}