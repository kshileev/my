
class Movie:
    def __init__(self, movie_id, rating):
        self.movie_id = movie_id
        self.rating = rating
        self.similarMovies = list()  # Similarity is bidirectional

    def __repr__(self):
        return self.movie_id + '=' + str(self.rating)

    def get_id(self):
        return self.movie_id

    def get_rating(self):
        return self.rating

    def add_similar_movie(self, movie):
        if movie not in self.similarMovies:
            self.similarMovies.append(movie)
            movie.add_similar_movie(self)

    def get_similar_movies(self):
        return self.similarMovies

    @staticmethod
    def get_movie_recommendations(movie, num):
        """Implement a function to return top rated movies in the network of movies
         * reachable from the current movie
         * eg:            A(Rating 1.2)
         *               /   \
         *            B(2.4)  C(3.6)
         *              \     /
         *               D(4.8)
         * In the above example edges represent similarity and the number is rating.
         * getMovieRecommendations(A,2) should return C and D (sorting order doesn't matter so it can also return D and C)
         * getMovieRecommendations(A,4) should return A, B, C, D (it can also return these in any order eg: B,C,D,A)
         * getMovieRecommendations(A,1) should return D. Note distance from A to D doesn't matter,
         *                             return the highest rated.
         *
         *     @param movie
         *     @param numTopRatedSimilarMovies
         *                      number of movies we want to return
         *     @return List of top rated similar movies
         */"""

        lst = movie.graph_traversal()
        return Movie.heap_max(num, lst)

    def graph_traversal(self):
        visited, stack = set(), [self]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)  # not deepcopy, memory consumption is tiny
                stack.extend(node.get_similar_movies())
        return visited

    @classmethod
    def heap_max(cls, num, lst):
        """Get num movies with max rating"""
        import heapq

        movies_with_max = lst[:num]  # memory consumption O(num)
        min_rating = 100000000 # big number more then any expected rating
        id_of_min_rating = 0

        for i, movie in enumerate(movies_with_max):
            if movie.get_rating() < min_rating:
                min_rating = movie.get_rating()
                id_of_min_rating = i

        for movie in lst:
            if movie.get_rating() > max_rating:
                movies_with_max[id_of_max_rating] = movie
                    heapq.heappop(heap)
                heapq.heappush(heap, item)
        return heap


"""
Assume that we might get cycled graph of movies. We first do depth graph traversal
here it takes O(n) time and O(n) memory
then we do usual mx-heap search which takes O(NLog(K)) time and O(k) memory
"""
if __name__ == '__main__':
    a = Movie(movie_id='A', rating=1.2)
    b = Movie(movie_id='B', rating=2.4)
    c = Movie(movie_id='C', rating=3.6)
    d = Movie(movie_id='D', rating=4.8)

    a.add_similar_movie(movie=b)
    a.add_similar_movie(movie=c)
    b.add_similar_movie(movie=d)
    c.add_similar_movie(movie=d)

    print Movie.get_movie_recommendations(movie=a, num=1)
